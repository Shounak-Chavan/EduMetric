"""
Pytest configuration and async fixtures for PostgreSQL testing.
"""

import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db


# PostgreSQL test database URL
TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)


# Create async SQLAlchemy engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)


# Create async session factory
TestingAsyncSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# Override FastAPI database dependency
async def override_get_db():

    async with TestingAsyncSessionLocal() as session:
        yield session


# Setup and cleanup database tables
@pytest_asyncio.fixture(scope="function")
async def setup_db():

    # Create tables before test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# FastAPI test client fixture
@pytest.fixture(scope="function")
def client(setup_db):

    # Override DB dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides after test
    app.dependency_overrides.clear()


# Mock JWT token fixture
@pytest.fixture(scope="function")
def auth_token():

    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0."
        "fake_token"
    )


# Authenticated client fixture
@pytest.fixture(scope="function")
def authenticated_client(client, auth_token):

    client.headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    yield client