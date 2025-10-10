from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlmodel import SQLModel


class Base(DeclarativeBase):
    metadata = SQLModel.metadata


UserId = UUID_ID


class User(SQLAlchemyBaseUserTableUUID, Base):
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_deleted = Column(Boolean(), default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
