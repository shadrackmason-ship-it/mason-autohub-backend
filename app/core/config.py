import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name = "Mason AutoHub API"
    database_url = os.getenv("DATABASE_URL", "sqlite:///./mason_autohub.db")
    secret_key = os.getenv("SECRET_KEY", "change-this-secret-before-production")
    algorithm = "HS256"
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
    cors_origins = [origin.strip() for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",") if origin.strip()]


settings = Settings()
