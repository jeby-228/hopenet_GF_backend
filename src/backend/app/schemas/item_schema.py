from pydantic import BaseModel


class CreateItemSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None


class UpdateItemSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
