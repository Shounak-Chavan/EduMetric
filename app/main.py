from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.security import HTTPBearer

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.routers_auth import router as auth_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    yield
    # shutdown (nothing for now)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
)
# THIS LINE ENABLES AUTHORIZE BUTTON
app.openapi_schema = None
security = HTTPBearer()

app.include_router(auth_router, tags=["Auth"])
register_exception_handlers(app)
