import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
        "http://localhost:5173",
        "http://localhost:3000", 
        "https://matrix-audit.netlify.app"
    ]
    
    # Tool Configuration
    SCAN_TIMEOUT: int = int(os.getenv("SCAN_TIMEOUT", "120"))
    
    # Default wordlists for directory scanning - use common wordlist locations
    # On Linux: /usr/share/wordlists, /usr/share/dirb/wordlists
    # On other systems, the scan will check availability and use dirsearch built-in wordlists
    WORDLISTS: dict = {
        "common": "/usr/share/wordlists/dirb/common.txt",
        "fast": "/usr/share/wordlists/dirb/small.txt", 
        "big": "/usr/share/wordlists/dirb/big.txt",
        "all": "/usr/share/wordlists/dirb/vulns/cgis.txt"
    }

# Create settings instance
settings = Settings()

# Clean up CORS origins (remove empty strings and strip whitespace)
settings.CORS_ORIGINS = [origin.strip() for origin in settings.CORS_ORIGINS if origin.strip()]