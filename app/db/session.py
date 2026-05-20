from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Always create async engine
# For SQLite: use sqlite+aiosqlite (requires aiosqlite package)
# For PostgreSQL: use postgresql+asyncpg

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    # For SQLite, disable pooling (not needed for file-based DB)
    poolclass=None if "sqlite" in settings.DATABASE_URL else None,
    echo=False,  # Set to True for SQL debugging
)

AsyncSessionLocal = sessionmaker(
    autoflush=False,
    class_=AsyncSession,
    autocommit=False,
    bind=engine,
    expire_on_commit=False
)

async def get_db():
    """Get database session for dependency injection."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()