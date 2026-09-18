from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies.auth import current_user
from app.database import get_db
from app.models.car import Car
from app.models.import_request import ImportRequest
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Administration"])


def require_admin(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Administrator access is required")
    return user


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    pending = list(db.scalars(select(Car).where(Car.status == "pending").order_by(Car.created_at.asc()).limit(100)))
    return {
        "stats": {
            "users": db.scalar(select(func.count()).select_from(User)),
            "cars": db.scalar(select(func.count()).select_from(Car)),
            "pending_cars": len(pending),
            "imports": db.scalar(select(func.count()).select_from(ImportRequest)),
        },
        "pending_listings": pending,
    }


class ListingReview(BaseModel):
    status: str


@router.patch("/cars/{car_id}")
def review_listing(car_id: int, payload: ListingReview, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if payload.status not in {"available", "rejected"}:
        raise HTTPException(400, "Status must be available or rejected")
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    car.status = payload.status
    db.commit()
    return {"id": car.id, "status": car.status}
