"""
Pytest configuration and async fixtures.
This file contains async setup and fixtures used across all tests.
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import your FastAPI app and database models
from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Configure pytest-asyncio
pytestmark = pytest.mark.asyncio

# Use async SQLite with aiosqlite driver
# Format: sqlite+aiosqlite:///path/to/db
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine with SQLite
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True for SQL debugging
)

# Create async session factory
TestingAsyncSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def override_get_db():
    """
    Override the get_db dependency for testing.
    Returns an async session from test database.
    """
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def setup_db():
    """
    Create and cleanup test database tables for each test.
    This runs before and after each test function.
    """
    # Create all tables before test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client(setup_db):
    """
    Create FastAPI TestClient with overridden database dependency.
    This is a synchronous fixture that uses the async setup_db fixture.
    """
    # Override the get_db dependency with our test version
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client (FastAPI TestClient is synchronous)
    test_client = TestClient(app)
    
    yield test_client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token():
    """
    Create a mock JWT token for testing protected routes.
    This is a fake token - in real scenarios, you'd generate a valid JWT.
    """
    # Example JWT token structure (not cryptographically valid)
    # header.payload.signature
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0.fake_token"
    return test_token


@pytest.fixture
def authenticated_client(client, auth_token):
    """
    Create a TestClient with authorization headers set.
    Use this fixture for testing protected/authenticated routes.
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
