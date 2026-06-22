import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    MIXPANEL_TOKEN: str = os.getenv("MIXPANEL_TOKEN", "")

    def validate(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is missing from .env file")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is missing from .env file")

settings = Settings()