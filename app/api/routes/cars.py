from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.dependencies.auth import current_user
from app.database import get_db
from app.models.car import Car
from app.models.user import User
from app.schemas.common import CarCreate

router = APIRouter(prefix="/cars", tags=["Cars"])

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB
MAGIC = {
    "image/jpeg": b"\xff\xd8\xff",
    "image/png":  b"\x89PNG\r\n\x1a\n",
    "image/webp": b"RIFF",
}


def _out(car: Car) -> dict:
    images = [car.image_url] if car.image_url else []
    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "name": f"{car.make} {car.model}",
        "year": car.year,
        "price": car.price,
        "mileage": car.mileage,
        "fuel_type": car.fuel_type,
        "transmission": car.transmission,
        "engine_cc": car.engine_cc,
        "body_type": car.body_type,
        "location": car.location,
        "image_url": car.image_url,
        "description": car.description,
        "condition": car.condition,
        "is_featured": car.is_featured,
        "is_import": car.is_import,
        "status": car.status,
        "owner_id": car.owner_id,
        "created_at": car.created_at,
        # frontend aliases
        "images": images,
        "brand": car.make,
        "body": car.body_type,
        "fuel": car.fuel_type,
        "trans": car.transmission,
        "power": f"{car.engine_cc} cc" if car.engine_cc else None,
    }


# ── Public endpoints ──────────────────────────────────────────────────────────

@router.get("")
def list_cars(
    q: str | None = None,
    make: str | None = None,
    body_type: str | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    min_year: int | None = Query(None, ge=1950),
    max_year: int | None = Query(None, le=2100),
    fuel_type: str | None = None,
    transmission: str | None = None,
    featured: bool | None = None,
    condition: str | None = None,
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Car).where(Car.status == "available")
    if q:
        t = f"%{q.strip()}%"
        stmt = stmt.where(or_(Car.make.ilike(t), Car.model.ilike(t), Car.location.ilike(t), Car.description.ilike(t)))
    if make:         stmt = stmt.where(Car.make.ilike(f"%{make}%"))
    if body_type:    stmt = stmt.where(Car.body_type.ilike(body_type))
    if fuel_type:    stmt = stmt.where(Car.fuel_type.ilike(fuel_type))
    if transmission: stmt = stmt.where(Car.transmission.ilike(transmission))
    if condition:    stmt = stmt.where(Car.condition == condition)
    if min_price is not None: stmt = stmt.where(Car.price >= min_price)
    if max_price is not None: stmt = stmt.where(Car.price <= max_price)
    if min_year is not None:  stmt = stmt.where(Car.year >= min_year)
    if max_year is not None:  stmt = stmt.where(Car.year <= max_year)
    if featured is not None:  stmt = stmt.where(Car.is_featured == featured)
    cars = list(db.scalars(stmt.order_by(Car.created_at.desc()).offset(offset).limit(limit)))
    return [_out(c) for c in cars]


@router.get("/filters")
def filter_options(db: Session = Depends(get_db)):
    available = select(Car).where(Car.status == "available")
    return {
        "makes":          sorted(set(db.scalars(available.with_only_columns(Car.make).distinct()))),
        "body_types":     sorted(set(db.scalars(available.with_only_columns(Car.body_type).distinct()))),
        "fuel_types":     sorted(set(db.scalars(available.with_only_columns(Car.fuel_type).distinct()))),
        "transmissions":  sorted(set(db.scalars(available.with_only_columns(Car.transmission).distinct()))),
        "locations":      sorted(set(db.scalars(available.with_only_columns(Car.location).distinct()))),
    }


@router.get("/autocomplete")
def autocomplete(q: str = Query(..., min_length=1, max_length=60), db: Session = Depends(get_db)):
    t = f"%{q.strip()}%"
    rows = db.execute(
        select(Car.make, Car.model)
        .where(Car.status == "available")
        .where(or_(Car.make.ilike(t), Car.model.ilike(t)))
        .distinct().limit(8)
    )
    return [{"label": f"{make} {model}", "make": make, "model": model} for make, model in rows]


@router.get("/{car_id}")
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if not car or car.status not in {"available", "sold"}:
        raise HTTPException(404, "Car not found")
    return _out(car)


@router.get("/{car_id}/similar")
def similar_cars(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    # Same body type first, then fill with recent listings
    same_body = list(db.scalars(
        select(Car)
        .where(Car.id != car_id, Car.status == "available", Car.body_type == car.body_type)
        .order_by(Car.created_at.desc()).limit(4)
    ))
    if len(same_body) < 4:
        exclude = {c.id for c in same_body} | {car_id}
        extras = list(db.scalars(
            select(Car)
            .where(Car.id.notin_(exclude), Car.status == "available")
            .order_by(Car.created_at.desc()).limit(4 - len(same_body))
        ))
        same_body.extend(extras)
    return [_out(c) for c in same_body]


# ── Authenticated endpoints ───────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_201_CREATED)
def create_car(
    payload: CarCreate,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    car = Car(**payload.model_dump(), owner_id=user.id, status="available")
    db.add(car)
    db.commit()
    db.refresh(car)
    return _out(car)


@router.patch("/{car_id}")
def update_car(
    car_id: int,
    payload: CarCreate,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    if car.owner_id != user.id:
        raise HTTPException(403, "You can only edit your own listings")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(car, field, value)
    db.commit()
    db.refresh(car)
    return _out(car)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    if car.owner_id != user.id:
        raise HTTPException(403, "You can only delete your own listings")
    db.delete(car)
    db.commit()


@router.post("/{car_id}/image")
async def upload_image(
    car_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    if car.owner_id != user.id:
        raise HTTPException(403, "You can only upload images to your own listings")
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(400, "Only JPG, PNG, or WebP images are accepted")
    contents = await file.read()
    await file.close()
    if not contents:
        raise HTTPException(400, "Empty file")
    if len(contents) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image must be under 5 MB")
    if not contents.startswith(MAGIC[file.content_type]):
        raise HTTPException(400, "File contents do not match the declared image type")
    ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[file.content_type]
    filename = f"{uuid.uuid4()}.{ext}"
    upload_dir = Path(__file__).resolve().parents[3] / "uploads"
    upload_dir.mkdir(exist_ok=True)
    (upload_dir / filename).write_bytes(contents)
    car.image_url = f"/uploads/{filename}"
    db.commit()
    db.refresh(car)
    return _out(car)
