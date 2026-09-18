from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import admin, auth, cars, imports, mechanics, services, spare_parts, users, vehicles
from app.core.config import settings
from app.database import Base, SessionLocal, engine
from sqlalchemy import inspect, text
from app import models  # noqa: F401 - registers SQLAlchemy models
from app.seed import seed_demo_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    if engine.dialect.name == "sqlite":
        _migrate_sqlite()
    with SessionLocal() as db:
        seed_demo_data(db)
    yield


def _migrate_sqlite():
    """Add columns that were introduced after the initial schema."""
    with engine.begin() as conn:
        existing = {c["name"] for c in inspect(engine).get_columns("cars")}
        if "owner_id" not in existing:
            conn.execute(text("ALTER TABLE cars ADD COLUMN owner_id INTEGER"))
        sb = {c["name"] for c in inspect(engine).get_columns("service_bookings")}
        if "location" not in sb:
            conn.execute(text("ALTER TABLE service_bookings ADD COLUMN location VARCHAR(120)"))
        if "total_price" not in sb:
            conn.execute(text("ALTER TABLE service_bookings ADD COLUMN total_price FLOAT"))


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
uploads_dir = Path(__file__).resolve().parents[1] / "uploads"
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(cars.router, prefix="/api/v1")
app.include_router(imports.router, prefix="/api/v1")
app.include_router(mechanics.router, prefix="/api/v1")
app.include_router(services.router, prefix="/api/v1")
app.include_router(spare_parts.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": settings.app_name}
