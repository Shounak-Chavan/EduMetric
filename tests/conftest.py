"""
Pytest configuration and async fixtures for PostgreSQL testing.
"""

import asyncio
import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)


# ✅ session-scoped so one engine lives for the entire test run
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def setup_db(test_engine):
    # Create all tables once for entire test session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop all tables after all tests done
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ✅ function-scoped client — fresh dependency override per test
@pytest.fixture(scope="function")
def client(setup_db, test_engine):

    TestingAsyncSessionLocal = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async def override_get_db():
        async with TestingAsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_token():
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6OTk5OTk5OTk5OX0."
        "fake_token"
    )


@pytest.fixture(scope="function")
def authenticated_client(client, auth_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {auth_token}"
    }
    yield client