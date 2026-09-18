from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.spare_part import SparePart
from app.models.cart_item import CartItem
from app.api.dependencies.auth import current_user
from app.models.user import User

router = APIRouter(tags=["Spare Parts"])


@router.get("/spare-parts")
def list_spare_parts(db: Session = Depends(get_db)):
    return list(db.scalars(select(SparePart).order_by(SparePart.name)))


class CartAdd(BaseModel):
    part_id: int
    quantity: int = Field(default=1, ge=1, le=100)


@router.post("/cart", status_code=status.HTTP_201_CREATED)
def add_to_cart(payload: CartAdd, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not db.get(SparePart, payload.part_id):
        raise HTTPException(404, "Spare part not found")
    item = db.scalar(select(CartItem).where(CartItem.user_id == user.id, CartItem.part_id == payload.part_id))
    if item:
        item.quantity = min(item.quantity + payload.quantity, 100)
    else:
        db.add(CartItem(user_id=user.id, part_id=payload.part_id, quantity=payload.quantity))
    db.commit()
    return {"added": True}
