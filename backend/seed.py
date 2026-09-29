"""Run once to create tables and add a few example items.

    python seed.py

Replace the whatsapp_product_id values with the real product IDs from
your WhatsApp Business catalog (Meta Commerce Manager) before using
this for real.
"""
from app import create_app
from models import Item, db

app = create_app()

SAMPLE_ITEMS = [
    dict(
        name="Anytime 30GB Monthly Package",
        category="Data Package",
        description="30GB anytime data, valid 30 days.",
        price=1490.00,
        image_url="",
        whatsapp_product_id="REPLACE_WITH_REAL_ID_1",
    ),
    dict(
        name="4G Prepaid SIM",
        category="SIM Plan",
        description="Prepaid SIM with free 2GB starter data.",
        price=100.00,
        image_url="",
        whatsapp_product_id="REPLACE_WITH_REAL_ID_2",
    ),
    dict(
        name="4G Wi-Fi Router",
        category="Device",
        description="Portable 4G Wi-Fi router, up to 10 devices.",
        price=12500.00,
        image_url="",
        whatsapp_product_id="REPLACE_WITH_REAL_ID_3",
    ),
]

with app.app_context():
    db.create_all()
    if Item.query.count() == 0:
        for data in SAMPLE_ITEMS:
            db.session.add(Item(**data))
        db.session.commit()
        print(f"Seeded {len(SAMPLE_ITEMS)} items.")
    else:
        print("Items already exist — skipping seed.")
