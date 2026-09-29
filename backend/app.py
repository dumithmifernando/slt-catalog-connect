from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from meta_catalog import MetaCatalogError, fetch_catalog_products, product_price
from models import Item, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)  # allow the React dev server / frontend origin to call this API

    def admin_required(view):
        @wraps(view)
        def protected(*args, **kwargs):
            expected = app.config.get("ADMIN_API_TOKEN")
            provided = request.headers.get("Authorization", "")
            if not expected or provided != f"Bearer {expected}":
                return jsonify({"error": "Admin authorization required"}), 401
            return view(*args, **kwargs)

        return protected

    @app.get("/api/items")
    def list_items():
        """Public: all active items, optionally filtered by ?category="""
        category = request.args.get("category")
        query = Item.query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        items = query.order_by(Item.category, Item.name).all()
        phone = app.config["WHATSAPP_BUSINESS_PHONE"]
        return jsonify([item.to_dict(phone) for item in items])

    @app.get("/api/items/<int:item_id>")
    def get_item(item_id):
        item = Item.query.get_or_404(item_id)
        phone = app.config["WHATSAPP_BUSINESS_PHONE"]
        return jsonify(item.to_dict(phone))

    @app.get("/api/categories")
    def list_categories():
        rows = db.session.query(Item.category).filter_by(is_active=True).distinct().all()
        return jsonify(sorted(r[0] for r in rows))

    # --- Admin endpoints ---

    @app.post("/api/items")
    @admin_required
    def create_item():
        data = request.get_json(force=True)
        required = ["name", "category", "whatsapp_product_id"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        item = Item(
            name=data["name"],
            category=data["category"],
            description=data.get("description"),
            price=data.get("price"),
            image_url=data.get("image_url"),
            whatsapp_product_id=data["whatsapp_product_id"],
            is_active=data.get("is_active", True),
        )
        db.session.add(item)
        db.session.commit()
        phone = app.config["WHATSAPP_BUSINESS_PHONE"]
        return jsonify(item.to_dict(phone)), 201

    @app.put("/api/items/<int:item_id>")
    @admin_required
    def update_item(item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json(force=True)
        for field in ["name", "category", "description", "price", "image_url", "whatsapp_product_id", "is_active"]:
            if field in data:
                setattr(item, field, data[field])
        db.session.commit()
        phone = app.config["WHATSAPP_BUSINESS_PHONE"]
        return jsonify(item.to_dict(phone))

    @app.delete("/api/items/<int:item_id>")
    @admin_required
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return "", 204

    @app.post("/api/admin/whatsapp/catalog/sync")
    @admin_required
    def sync_whatsapp_catalog():
        catalog_id = app.config.get("META_CATALOG_ID")
        access_token = app.config.get("META_ACCESS_TOKEN")
        if not catalog_id or not access_token:
            return jsonify({"error": "META_CATALOG_ID and META_ACCESS_TOKEN must be configured"}), 503

        try:
            products = fetch_catalog_products(
                catalog_id,
                access_token,
                app.config["META_GRAPH_API_VERSION"],
            )
        except MetaCatalogError as error:
            return jsonify({"error": str(error)}), 502

        created = 0
        updated = 0
        for product in products:
            product_id = product.get("id")
            if not product_id or product.get("availability") == "out of stock":
                continue

            item = Item.query.filter_by(whatsapp_product_id=product_id).first()
            if item is None:
                item = Item(
                    whatsapp_product_id=product_id,
                    category="WhatsApp Catalog",
                )
                db.session.add(item)
                created += 1
            else:
                updated += 1

            item.name = product.get("name") or item.name or product_id
            item.description = product.get("description") or item.description
            item.price = product_price(product)
            item.image_url = product.get("image_url") or item.image_url
            item.is_active = True

        db.session.commit()
        return jsonify({"created": created, "updated": updated, "received": len(products)})

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
