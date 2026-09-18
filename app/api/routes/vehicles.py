"""Vehicle-data endpoints backed by NHTSA's free vPIC service."""
import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException

from app.schemas.common import VinDecodeOut, VinDecodeRequest

router = APIRouter(prefix="/vehicles", tags=["Vehicle data"])


def value(result: dict, key: str) -> str | None:
    raw = result.get(key)
    if not raw or raw in {"Not Applicable", "Not Available", "Unknown"}:
        return None
    return str(raw).strip()


def fuel_type(raw: str | None) -> str | None:
    text = (raw or "").lower()
    if "electric" in text: return "Electric"
    if "hybrid" in text: return "Hybrid"
    if "diesel" in text: return "Diesel"
    if "gasoline" in text or "petrol" in text: return "Petrol"
    if "liquefied petroleum" in text or text == "lpg": return "LPG"
    return None


def transmission(raw: str | None) -> str | None:
    text = (raw or "").lower()
    if "automatic" in text: return "Automatic"
    if "manual" in text: return "Manual"
    if "continuously variable" in text or "cvt" in text: return "CVT"
    return None


@router.post("/decode-vin", response_model=VinDecodeOut)
def decode_vin(payload: VinDecodeRequest):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{quote(payload.vin)}?format=json"
    try:
        with urlopen(url, timeout=8) as response:
            result = json.load(response).get("Results", [])[0]
    except (URLError, TimeoutError, IndexError, json.JSONDecodeError) as exc:
        raise HTTPException(503, "Vehicle lookup is temporarily unavailable. Enter details manually.") from exc

    year_raw, litres_raw = value(result, "ModelYear"), value(result, "DisplacementL")
    try:
        year = int(year_raw) if year_raw else None
        engine_cc = round(float(litres_raw) * 1000) if litres_raw else None
    except ValueError:
        year, engine_cc = None, None
    return VinDecodeOut(
        vin=payload.vin, make=value(result, "Make"), model=value(result, "Model"),
        year=year if year and 1980 <= year <= 2030 else None,
        body_type=value(result, "BodyClass"), fuel_type=fuel_type(value(result, "FuelTypePrimary")),
        transmission=transmission(value(result, "TransmissionStyle")),
        engine_cc=engine_cc if engine_cc and 50 <= engine_cc <= 10000 else None,
        manufacturer=value(result, "Manufacturer"),
    )
