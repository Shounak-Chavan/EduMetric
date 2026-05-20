from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Check if using SQLite (for testing) - SQLite doesn't support async
is_sqlite = settings.DATABASE_URL and settings.DATABASE_URL.startswith("sqlite")

if not is_sqlite and settings.DATABASE_URL:
    # Use async engine for PostgreSQL
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )
    
    AsyncSessionLocal = sessionmaker(
        autoflush=False,
        class_=AsyncSession,
        autocommit=False,
        bind=engine
    )
    
    async def get_db():
        db = AsyncSessionLocal()
        try:
            yield db
        finally:
            await db.close()
else:
    # For testing with SQLite or when DATABASE_URL is not set
    # Create a dummy get_db function that will be overridden by conftest.py
    async def get_db():
        """
        Placeholder for testing. This will be overridden by conftest.py
        """
        yield None