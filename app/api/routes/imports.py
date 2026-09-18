from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.import_request import ImportRequest
from app.api.dependencies.auth import current_user
from app.models.user import User

router = APIRouter(prefix="/import-requests", tags=["Import Requests"])


class ImportRequestCreate(BaseModel):
    origin_country: str
    vehicle_price_usd: float
    year: str
    engine_size_cc: int
    fuel_type: str
    estimated_total_usd: float


@router.post("", status_code=status.HTTP_201_CREATED)
def create_import_request(payload: ImportRequestCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    req = ImportRequest(**payload.model_dump(), user_id=user.id)
    db.add(req); db.commit(); db.refresh(req)
    return {
        "id": req.id,
        "status": req.status,
        "origin_country": req.origin_country,
        "vehicle_price_usd": req.vehicle_price_usd,
        "estimated_total_usd": req.estimated_total_usd,
        "name": f"Import from {req.origin_country}",
        "origin": req.origin_country,
        "eta": "6–8 weeks",
        "created_at": req.created_at,
    }
