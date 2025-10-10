from datetime import datetime
import typing as t

from sqlmodel import Column
from sqlmodel import DateTime
from sqlmodel import Field
from sqlmodel import SQLModel
from sqlmodel import func


class Item(SQLModel, table=True):
    __tablename__: t.ClassVar[str] = 'item'  # pyright: ignore[reportIncompatibleVariableOverride]

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))

    id: int = Field(primary_key=True, nullable=False)

    name: str
    description: str
    category: str
    price: int
