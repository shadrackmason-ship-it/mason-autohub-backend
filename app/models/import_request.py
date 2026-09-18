from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ImportRequest(Base):
    __tablename__ = "import_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    origin_country: Mapped[str] = mapped_column(String(100))
    vehicle_price_usd: Mapped[float] = mapped_column(Float)
    year: Mapped[str] = mapped_column(String(20))
    engine_size_cc: Mapped[int] = mapped_column(Integer)
    fuel_type: Mapped[str] = mapped_column(String(30))
    estimated_total_usd: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
