from datetime import datetime
import typing as t

from pydantic import HttpUrl
from sqlmodel import Column
from sqlmodel import DateTime
from sqlmodel import Field
from sqlmodel import SQLModel
from sqlmodel import func

from ..enums.task_enum import TaskStatus
from .user_model import UserId


# TODO: index, varchar length, ...


class Task(SQLModel, table=True):
    __tablename__: t.ClassVar[str] = 'task'  # pyright: ignore[reportIncompatibleVariableOverride]

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()))
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))

    id: int = Field(primary_key=True)

    creator_id: UserId | None = Field(default=None, foreign_key='user.id', index=True)

    title: str = Field(description='標題')
    status: t.Annotated[str, TaskStatus] | None = Field(description='任務狀態')
    description: str | None = Field(description='簡單敘述')
    weight: int = Field(default=50, description='預設顯示排序')
    start_at: datetime | None = Field(description='開始時間', sa_column=Column(DateTime(timezone=True)))
    deadline: datetime | None = Field(description='截止時間', sa_column=Column(DateTime(timezone=True)))
    contact_number: str | None = Field(description='聯絡電話')
    registration_location: str | None = Field(description='報到地點')
    registration_location_url: t.Annotated[str, HttpUrl] | None = Field(description='報到地點參考連結')
    work_location: str | None = Field(description='工作地點')
    work_location_url: t.Annotated[str, HttpUrl] | None = Field(description='工作地點參考連結')
    maximum_number_of_people: int | None = Field(description='最大人數')
