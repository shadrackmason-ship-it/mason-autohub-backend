"""Promote one existing user to admin. Run manually from the backend folder."""
import sys
from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User


if len(sys.argv) != 2:
    raise SystemExit("Usage: ./.venv/bin/python promote_admin.py your-email@example.com")

email = sys.argv[1].strip().lower()
with SessionLocal() as db:
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        raise SystemExit("No user exists with that email. Register the account first.")
    user.role = "admin"
    db.commit()
    print(f"Admin access granted to {email}.")
