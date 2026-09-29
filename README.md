# SLT Item Catalog → WhatsApp Business

A small system: customers browse item cards (data packages, SIM plans,
devices) on a React site, and tapping a card opens that exact product
inside your WhatsApp Business catalog.

## How the WhatsApp link works

WhatsApp Business catalog products each get a shareable deep link:

```
https://wa.me/p/<product_id>/<business_phone_number>
```

Opening it takes the customer straight into WhatsApp, showing that one
product from your catalog, with a button to message you about it.

This means each item needs two things set up **on Meta's side first**,
before it can appear correctly here:

1. Your WhatsApp Business Account needs a **catalog** (set up via
   [Meta Commerce Manager](https://business.facebook.com/commerce/)
   or the WhatsApp Business app's Catalog tab).
2. Each product you add to that catalog gets a **product ID** — copy
   it into this system's `whatsapp_product_id` field for the matching
   item (see `backend/seed.py` for where that goes).

This app doesn't create catalog products for you. It can import products
that already exist in the catalog through Meta's Graph API, store the
product mapping, and build the correct link for each card.

## Project layout

```
backend/    Flask API + PostgreSQL models
frontend/   React site (Vite)
```

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# create a Postgres database first, e.g.:
#   createdb slt_catalog

# create .env with DATABASE_URL, WHATSAPP_BUSINESS_PHONE,
# ADMIN_API_TOKEN, META_CATALOG_ID, and META_ACCESS_TOKEN
python seed.py                  # creates tables + example items
python app.py                   # runs on http://localhost:5000
```

Edit the items in `seed.py` (or use the authenticated API below) with
your real catalog product IDs.

### API

| Method | Path              | Purpose                          |
| ------ | ----------------- | -------------------------------- |
| GET    | `/api/items`      | list active items (`?category=`) |
| GET    | `/api/items/<id>` | single item                      |
| POST   | `/api/items`      | add an item                      |
| PUT    | `/api/items/<id>` | edit an item                     |
| DELETE | `/api/items/<id>` | remove an item                   |
| GET    | `/api/categories` | distinct category names          |

Write endpoints require `Authorization: Bearer <ADMIN_API_TOKEN>`.

### Import products from Meta

Create a Meta app with catalog read access, obtain a system-user access
token, and set `META_CATALOG_ID` and `META_ACCESS_TOKEN` in the backend
environment. Then run:

```bash
curl -X POST http://localhost:5000/api/admin/whatsapp/catalog/sync \
   -H "Authorization: Bearer YOUR_ADMIN_API_TOKEN"
```

The sync imports available products and matches future runs by
`whatsapp_product_id`. Keep the Meta access token server-side; never put
it in the React app or commit it to source control.

## Frontend setup

```bash
cd frontend
npm install
npm run dev                     # runs on http://localhost:5173, proxies /api to :5000
```

For production, `npm run build` outputs static files in `frontend/dist`
that you can serve from any static host or from Flask itself.

## Adding items going forward

1. Add the product in Meta Commerce Manager.
2. Run the catalog sync, or use the authenticated item API for manual
   categorization and overrides.
3. It shows up on the site immediately, linking to the right product.
