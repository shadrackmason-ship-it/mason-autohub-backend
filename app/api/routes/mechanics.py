from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mechanic import Mechanic
from app.schemas.common import MechanicOut

router = APIRouter(prefix="/mechanics", tags=["Mechanics"])

@router.get("", response_model=list[MechanicOut])
def list_mechanics(location: str | None = None, open_now: bool | None = None,
                   limit: int = Query(24, ge=1, le=100), db: Session = Depends(get_db)):
    statement = select(Mechanic)
    if location: statement = statement.where(Mechanic.location.ilike(f"%{location}%"))
    if open_now is not None: statement = statement.where(Mechanic.is_open == open_now)
    return list(db.scalars(statement.order_by(Mechanic.rating.desc()).limit(limit)))
