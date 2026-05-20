import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App
    PROJECT_NAME = os.getenv("APP_NAME", "EduMetric")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # JWT
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # Database
    # Supports:
    # - postgresql+asyncpg://user:password@localhost/dbname (production)
    # - sqlite+aiosqlite:///:memory: (testing)
    # - sqlite+aiosqlite:///./test.db (file-based testing)
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()

# Validate required settings
if not settings.JWT_SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Example usage
# print(settings.PROJECT_NAME)      # EduMetric