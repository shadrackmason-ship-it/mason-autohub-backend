from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class SparePart(Base):
    __tablename__ = "spare_parts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    brand: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(60), index=True)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    img: Mapped[str | None] = mapped_column(String(500), nullable=True)
