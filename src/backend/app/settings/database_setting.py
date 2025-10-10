import typing as t

from pydantic import Field
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy import make_url


class Settings(BaseSettings):
    echo: t.ClassVar[bool] = False
    expire_on_commit: t.ClassVar[bool] = True

    postgres_dsn: PostgresDsn = Field(default=..., validation_alias='POSTGRES_DSN')

    @property
    def _postgres_url(self) -> URL:
        s = self.postgres_dsn.unicode_string()
        return make_url(s)

    @property
    def database_url(self) -> str:
        s = self._postgres_url.render_as_string(hide_password=False)
        return s

    @property
    def sync_database_url(self) -> str:
        u = self._postgres_url.set(drivername='postgresql')
        s = u.render_as_string(hide_password=False)
        return s


database_settings = Settings()
