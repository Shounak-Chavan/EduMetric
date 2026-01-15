import uuid
from enum import Enum

from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class UserRole(str, Enum):
    recruiter = "recruiter"
    candidate = "candidate"


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    role = Column(SQLEnum(UserRole), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
