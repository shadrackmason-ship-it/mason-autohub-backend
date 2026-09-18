# Mason AutoHub backend

FastAPI API powering the Mason AutoHub React frontend.

## Start locally

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

The API starts at `http://localhost:8000`; interactive documentation is at `/docs`.
It creates a local SQLite database with demo inventory on first run. Set `DATABASE_URL` to a PostgreSQL connection string before deployment.

## Frontend endpoints

- `GET /api/v1/cars?q=prado&body_type=SUV&max_price=6000000`
- `GET /api/v1/cars/autocomplete?q=toy`
- `GET /api/v1/cars/filters`
- `GET /api/v1/cars?featured=true` and `?latest_import=true`
- `POST /api/v1/imports/calculate`
- `GET /api/v1/mechanics?location=Kitengela&open_now=true`
- `POST /api/v1/service-bookings`
- `POST /api/v1/auth/register`, `POST /api/v1/auth/login` (form fields: `username`, `password`)

Set `CORS_ORIGINS` in `.env` to the URL of your React app, for example `http://localhost:5173`.

## Admin access

Register your account normally, then promote only that trusted account from the
backend server (never through the public registration form):

```bash
./.venv/bin/python promote_admin.py your-email@example.com
```

Log out and sign in again. The Admin button will appear in the navigation.
Admins can review pending listings at `/admin`; approved listings become public.
