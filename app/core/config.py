import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = 'resume_screening_backend'
    API_KEY = os.getenv('API_KEY')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',60))

    RECRUITER_INVITE_CODE = os.getenv('RECRUITER_INVITE_CODE')
    DATABASE_URL = os.getenv('DATABASE_URL')

settings = Settings()
