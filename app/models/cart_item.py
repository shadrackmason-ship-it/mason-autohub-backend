from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("user_id", "part_id", name="uq_cart_user_part"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("spare_parts.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
