from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: SecretStr = Field(default=..., validation_alias='SECRET_KEY')


user_settings = Settings()
