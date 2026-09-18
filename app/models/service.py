from datetime import date, datetime
from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ServiceBooking(Base):
    __tablename__ = "service_bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(30))
    service_type: Mapped[str] = mapped_column(String(200))
    mechanic_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    booking_date: Mapped[date] = mapped_column(Date)
    booking_time: Mapped[str] = mapped_column(String(10))
    total_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
