import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App
    PROJECT_NAME = os.getenv("APP_NAME", "EduMetric")
    DEBUG = os.getenv("DEBUG") == "True"

    # JWT
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()

# Validate required settings only in production
if not settings.JWT_SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

# Database URL is optional during testing (tests use their own database)
if not settings.DATABASE_URL and not os.getenv("PYTEST_CURRENT_TEST"):
    # Only raise error if not in test environment
    pass

# Example usage
# print(settings.PROJECT_NAME)      # EduMetric