import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SCAN_TIMEOUT: int = int(os.getenv("SCAN_TIMEOUT", "60"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://matrix-audit.netlify.app"
    ]

settings = Settings()
settings.CORS_ORIGINS = [o.strip() for o in settings.CORS_ORIGINS if o.strip()]
