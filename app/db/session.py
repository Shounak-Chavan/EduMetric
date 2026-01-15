from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping = True,
)

AsyncSessionLocal = sessionmaker(
    autoflush=False,
    class_=AsyncSession,
    autocommit = False,
    bind = engine
)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()