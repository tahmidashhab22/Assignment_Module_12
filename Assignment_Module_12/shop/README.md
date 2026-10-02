# Shop Product API

Django + Django REST Framework API for a small online shop.
Anyone can view products; only token-authenticated users can add them.

## Install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run migrations
```bash
python manage.py migrate
```

## Create a test user and token
```bash
python manage.py createsuperuser --username testuser --email test@example.com
python manage.py drf_create_token testuser     # prints the token
```

## Start the server
```bash
python manage.py runserver
```

## Endpoints
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/api/products/` | none | Paginated list (5 per page, ordered by id, `?page=2`) |
| POST | `/api/products/` | `Authorization: Token YOUR_TOKEN` | Create a product |

Example POST body (Postman: Body -> raw -> JSON):
```json
{"name": "Notebook", "description": "A notebook with 100 pages.", "price": "120.00", "stock": 25}
```

Validation: name not empty, price > 0, stock a whole number >= 0.

## Run automated tests
```bash
python manage.py test
```

## Screenshots
Replace/add your own Postman screenshots in `screenshots/`.
`screenshots/api_test_transcript.txt` holds real request/response output for every required test.
