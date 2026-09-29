import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """App configuration, loaded from environment variables.

    Copy .env.example to .env and fill in real values before running.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://slt_user:slt_password@localhost:5432/slt_catalog",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # The WhatsApp Business phone number customers will be sent to,
    # in international format with no "+" or spaces, e.g. "94771234567".
    WHATSAPP_BUSINESS_PHONE = os.environ.get("WHATSAPP_BUSINESS_PHONE", "94771234567")
    META_CATALOG_ID = os.environ.get("META_CATALOG_ID")
    META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
    META_GRAPH_API_VERSION = os.environ.get("META_GRAPH_API_VERSION", "v23.0")
    ADMIN_API_TOKEN = os.environ.get("ADMIN_API_TOKEN")
