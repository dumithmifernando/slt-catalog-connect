from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    """A single item card: a data package, SIM plan, or device.

    whatsapp_product_id is the product ID assigned to this item inside
    Meta Commerce Manager / WhatsApp Business catalog. It's what lets a
    card link straight to that one product in the WhatsApp catalog via:
        https://wa.me/p/<whatsapp_product_id>/<business_phone>
    You get this ID after adding the item to your WhatsApp catalog
    (see README.md for how).
    """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)  # e.g. "Data Package", "SIM Plan", "Device"
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    whatsapp_product_id = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self, business_phone: str):
        has_valid_product_id = bool(
            self.whatsapp_product_id
            and not self.whatsapp_product_id.upper().startswith("REPLACE_WITH_REAL_ID")
        )
        whatsapp_url = (
            f"https://wa.me/p/{self.whatsapp_product_id}/{business_phone}"
            if has_valid_product_id
            else f"https://wa.me/{business_phone}"
        )
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": float(self.price) if self.price is not None else None,
            "image_url": self.image_url,
            "whatsapp_url": whatsapp_url,
            "is_active": self.is_active,
        }
