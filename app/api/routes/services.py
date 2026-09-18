from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.service import ServiceBooking
from app.schemas.common import BookingCreate, BookingOut

router = APIRouter(prefix="/service-bookings", tags=["Service bookings"])

@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = ServiceBooking(**payload.model_dump())
    db.add(booking); db.commit(); db.refresh(booking)
    return booking
