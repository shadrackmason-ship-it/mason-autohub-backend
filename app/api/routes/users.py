from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.dependencies.auth import current_user
from app.database import get_db
from app.models.user import User
from app.models.car import Car
from app.models.import_request import ImportRequest
from app.models.saved_car import SavedCar

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


def _car_dict(car: Car) -> dict:
    """Serialize a Car to a dict the frontend normalizeCar() can consume."""
    images = [car.image_url] if car.image_url else []
    return {
        "id": car.id, "make": car.make, "model": car.model,
        "name": f"{car.make} {car.model}",
        "year": car.year, "price": car.price, "mileage": car.mileage,
        "fuel_type": car.fuel_type, "transmission": car.transmission,
        "engine_cc": car.engine_cc, "body_type": car.body_type,
        "location": car.location, "condition": car.condition,
        "status": car.status, "images": images,
        "image_url": car.image_url,
        "brand": car.make, "body": car.body_type,
        "fuel": car.fuel_type, "trans": car.transmission,
        "power": f"{car.engine_cc} cc" if car.engine_cc else None,
        "plate": getattr(car, "plate", None),
        "created_at": car.created_at,
    }


@router.patch("/me")
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.phone is not None:
        user.phone = payload.phone
    db.commit()
    db.refresh(user)
    return {"id": user.id, "full_name": user.full_name, "email": user.email, "phone": user.phone, "role": user.role}


@router.get("/me/cars")
def my_cars(db: Session = Depends(get_db), user: User = Depends(current_user)):
    cars = list(db.scalars(select(Car).where(Car.owner_id == user.id).order_by(Car.created_at.desc())))
    return [_car_dict(c) for c in cars]


@router.get("/me/saved")
def my_saved(db: Session = Depends(get_db), user: User = Depends(current_user)):
    cars = list(db.scalars(select(Car).join(SavedCar, SavedCar.car_id == Car.id).where(SavedCar.user_id == user.id)))
    return [_car_dict(c) for c in cars]


@router.post("/me/saved/{car_id}", status_code=status.HTTP_201_CREATED)
def save_car(car_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not db.get(Car, car_id):
        raise HTTPException(404, "Car not found")
    if not db.scalar(select(SavedCar).where(SavedCar.user_id == user.id, SavedCar.car_id == car_id)):
        db.add(SavedCar(user_id=user.id, car_id=car_id)); db.commit()
    return {"saved": True}


@router.delete("/me/saved/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsave_car(car_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    saved = db.scalar(select(SavedCar).where(SavedCar.user_id == user.id, SavedCar.car_id == car_id))
    if saved:
        db.delete(saved); db.commit()


@router.get("/me/imports")
def my_imports(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = list(db.scalars(select(ImportRequest).where(ImportRequest.user_id == user.id).order_by(ImportRequest.created_at.desc())))
    return [
        {
            "id": r.id, "status": r.status,
            "origin_country": r.origin_country,
            "vehicle_price_usd": r.vehicle_price_usd,
            "estimated_total_usd": r.estimated_total_usd,
            "name": f"Import from {r.origin_country}",
            "origin": r.origin_country,
            "eta": "6–8 weeks",
            "created_at": r.created_at,
        }
        for r in rows
    ]
