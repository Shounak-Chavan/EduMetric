"""
Pytest configuration and fixtures.
This file contains setup and fixtures used across all tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Import your FastAPI app and database models
from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Use PostgreSQL test database (matches GitHub Actions setup)
# Falls back to SQLite if PostgreSQL not available locally
database_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/edumetric_test"
)

# For local testing with SQLite, you can use:
# SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
# But GitHub Actions uses PostgreSQL

SQLALCHEMY_TEST_DATABASE_URL = database_url

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_TEST_DATABASE_URL else {}
)

# Create tables for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create a clean database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with overridden database dependency."""
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token():
    """
    Create a test JWT token.
    This is a mock token - in a real scenario, you'd generate a valid JWT.
    """
    # For testing, we'll create a simple token
    # In your actual implementation, import and use your token creation function
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0.fake_token"
    return test_token


@pytest.fixture
def authenticated_client(client, auth_token):
    """
    Create a test client with authorization headers set.
    Use this for testing protected routes.
    """
    client.headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    return client
