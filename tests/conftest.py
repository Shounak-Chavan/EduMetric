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


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingAsyncSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def override_get_db():
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(setup_db):
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
        **client.headers,                   # ✅ preserve existing headers
        "Authorization": f"Bearer {auth_token}"
    }

    yield client                            # ✅ typo fixed