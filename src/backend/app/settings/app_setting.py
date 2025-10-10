import typing as t

from pydantic import AnyUrl
from pydantic import BeforeValidator
from pydantic import Field
from pydantic_settings import BaseSettings


def _parse_cors(v: t.Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',') if i.strip()]
    if isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    API_V1_STR: t.ClassVar[str] = '/api/v1'

    PROJECT_NAME: str = Field(default=..., validation_alias='PROJECT_NAME')

    BACKEND_CORS_ORIGINS: t.Annotated[list[AnyUrl] | str, BeforeValidator(_parse_cors)] = Field(
        default=..., validation_alias='BACKEND_CORS_ORIGINS'
    )

    FRONTEND_HOST: str = Field(default='http://localhost:5173', validation_alias='FRONTEND_HOST')

    @property
    def all_cors_origins(self) -> list[str]:
        return list({str(origin).rstrip('/') for origin in self.BACKEND_CORS_ORIGINS} | {self.FRONTEND_HOST})


app_settings = Settings()
