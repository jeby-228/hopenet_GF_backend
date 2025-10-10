from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from ..enums.task_enum import TaskStatus


class CreateTaskSchema(BaseModel):
    title: str = Field(default=..., description='標題')
    status: TaskStatus | None = Field(default=None, description='任務狀態')
    description: str | None = Field(default=None, description='簡單敘述')
    weight: int | None = Field(default=None, description='預設顯示排序')
    start_at: datetime | None = Field(default=None, description='開始時間')
    deadline: datetime | None = Field(default=None, description='截止時間')
    contact_number: str | None = Field(default=None, description='聯絡電話')
    registration_location: str | None = Field(default=None, description='報到地點')
    registration_location_url: HttpUrl | None = Field(default=None, description='報到地點參考連結')
    work_location: str | None = Field(default=None, description='工作地點')
    work_location_url: HttpUrl | None = Field(default=None, description='工作地點參考連結')
    maximum_number_of_people: int | None = Field(default=None, description='最大人數')


class UpdateTaskSchema(BaseModel):
    title: str | None = Field(default=None, description='標題')
    status: TaskStatus | None = Field(default=None, description='任務狀態')
    description: str | None = Field(default=None, description='簡單敘述')
    weight: int | None = Field(default=None, description='預設顯示排序')
    start_at: datetime | None = Field(default=None, description='開始時間')
    deadline: datetime | None = Field(default=None, description='截止時間')
    contact_number: str | None = Field(default=None, description='聯絡電話')
    registration_location: str | None = Field(default=None, description='報到地點')
    registration_location_url: HttpUrl | None = Field(default=None, description='報到地點參考連結')
    work_location: str | None = Field(default=None, description='工作地點')
    work_location_url: HttpUrl | None = Field(default=None, description='工作地點參考連結')
    maximusm_number_of_people: int | None = Field(default=None, description='最大人數')
