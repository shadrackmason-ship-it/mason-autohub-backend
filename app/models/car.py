from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Car(Base):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    make: Mapped[str] = mapped_column(String(60), index=True)
    model: Mapped[str] = mapped_column(String(80), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    price: Mapped[float] = mapped_column(Float, index=True)
    mileage: Mapped[int] = mapped_column(Integer, default=0)
    fuel_type: Mapped[str] = mapped_column(String(30))
    transmission: Mapped[str] = mapped_column(String(30))
    engine_cc: Mapped[int] = mapped_column(Integer)
    body_type: Mapped[str] = mapped_column(String(40), index=True)
    location: Mapped[str] = mapped_column(String(100), index=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    condition: Mapped[str] = mapped_column(String(30), default="used")
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_import: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="available", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
