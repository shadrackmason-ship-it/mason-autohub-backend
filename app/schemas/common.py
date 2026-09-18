from datetime import date, datetime
import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CarCreate(BaseModel):
    make: str
    model: str
    year: int = Field(ge=1950, le=2100)
    price: float = Field(ge=0)
    mileage: int = Field(default=0, ge=0)
    fuel_type: str
    transmission: str
    engine_cc: int = Field(default=0, ge=0)
    body_type: str = "Other"
    location: str = "Kenya"
    image_url: str | None = None
    description: str | None = None
    condition: str = "used"
    is_featured: bool = False
    is_import: bool = False


class CarOut(CarCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    created_at: datetime


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = None
    password: str = Field(min_length=8, max_length=128)
    role: str = "buyer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VinDecodeRequest(BaseModel):
    vin: str = Field(min_length=17, max_length=17)

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, value: str) -> str:
        vin = value.strip().upper()
        if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
            raise ValueError("Enter a valid 17-character VIN")
        return vin


class VinDecodeOut(BaseModel):
    vin: str
    make: str | None = None
    model: str | None = None
    year: int | None = None
    body_type: str | None = None
    fuel_type: str | None = None
    transmission: str | None = None
    engine_cc: int | None = None
    manufacturer: str | None = None


class MechanicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    location: str
    specialty: str
    rating: float
    review_count: int
    phone: str
    is_open: bool


class BookingCreate(BaseModel):
    customer_name: str
    phone: str
    service_type: str
    mechanic_id: int | None = None
    location: str | None = None
    booking_date: date
    booking_time: str
    total_price: float | None = None


class BookingOut(BookingCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    created_at: datetime


class ImportCalculationRequest(BaseModel):
    car_price: float = Field(gt=0, description="Vehicle price in KES")
    country: str
    year: int = Field(ge=1950, le=2100)
    engine_cc: int = Field(gt=0)
    fuel_type: str


class ImportCalculation(BaseModel):
    car_price: float
    shipping: float
    import_duty: float
    excise_duty: float
    vat: float
    idf: float
    railway_levy: float
    port_charges: float
    total_cost: float
    currency: str = "KES"
    disclaimer: str
