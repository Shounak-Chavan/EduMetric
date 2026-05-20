"""
Pytest configuration and async fixtures for PostgreSQL testing.
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Use same PostgreSQL URL as configured in environment
# In GitHub Actions, this will be: postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
# Locally, update your .env to use a test database
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)

# Create async engine for testing (same as production setup)
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
)

# Create async session factory for testing
TestingAsyncSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def override_get_db():
    """
    Override database dependency for testing.
    Returns an async session from test database.
    """
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def setup_db():
    """
    Create and cleanup test database tables for each test.
    
    This fixture:
    1. Creates all tables before the test runs
    2. Yields control to the test
    3. Drops all tables after the test completes
    
    Ensures clean, isolated test environment.
    """
    # Create all tables before test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop all tables after test (cleanup)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(setup_db):
    """
    Create FastAPI TestClient with overridden database dependency.
    
    This is a synchronous fixture because:
    - FastAPI TestClient is synchronous
    - It handles async route execution internally
    - setup_db is awaited by pytest-asyncio before this runs
    
    Usage:
        def test_endpoint(self, client):
            response = client.get("/api/endpoint")
            assert response.status_code == 200
    """
    # Override the get_db dependency with test version
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token():
    """
    Create a mock JWT token for testing protected routes.
    
    This is a fake token structure (not cryptographically valid).
    In production, you would generate real tokens using your security functions.
    
    Usage:
        def test_protected(self, authenticated_client):
            response = authenticated_client.get("/api/protected")
            assert response.status_code == 200
    """
    # JWT token format: header.payload.signature
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0.fake_token"
    return test_token


@pytest.fixture
def authenticated_client(client, auth_token):
    """
    Create a TestClient with authorization headers set.
    
    This fixture automatically adds Bearer token to all requests.
    Use this for testing endpoints that require authentication.
    
    Usage:
        def test_protected_route(self, authenticated_client):
            response = authenticated_client.get("/api/protected")
            assert response.status_code == 200
    """
    client.headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    return client


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
