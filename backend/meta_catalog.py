from decimal import Decimal, InvalidOperation

import requests


class MetaCatalogError(RuntimeError):
    pass


def fetch_catalog_products(catalog_id: str, access_token: str, graph_api_version: str):
    url = f"https://graph.facebook.com/{graph_api_version}/{catalog_id}/products"
    params = {
        "access_token": access_token,
        "fields": "id,name,description,price,currency,image_url,availability,retailer_id",
        "limit": 100,
    }
    products = []

    while url:
        response = requests.get(url, params=params, timeout=30)
        if not response.ok:
            try:
                details = response.json().get("error", {}).get("message", response.text)
            except ValueError:
                details = response.text
            raise MetaCatalogError(f"Meta catalog request failed: {details}")

        payload = response.json()
        products.extend(payload.get("data", []))
        url = payload.get("paging", {}).get("next")
        params = None

    return products


def product_price(product):
    raw_price = product.get("price")
    if raw_price in (None, ""):
        return None
    try:
        return Decimal(str(raw_price))
    except (InvalidOperation, ValueError):
        return None