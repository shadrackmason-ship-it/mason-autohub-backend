from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    location: Mapped[str] = mapped_column(String(100), index=True)
    specialty: Mapped[str] = mapped_column(String(150))
    rating: Mapped[float] = mapped_column(Float, default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    phone: Mapped[str] = mapped_column(String(30))
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
