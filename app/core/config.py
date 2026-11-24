from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "DevOps Lab API"
    APP_VERSION: str = "0.2.0"

    APP_ENV: Literal[
        "development",
        "testing",
        "production",
    ] = "development"

    DEBUG: bool = False
    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    DB_HOST: str = "localhost"
    DB_PORT: int = Field(default=5432, ge=1, le=65535)
    DB_NAME: str = "devops_lab"
    DB_USER: str = "devops_user"
    DB_PASSWORD: SecretStr = SecretStr("")

    DB_POOL_SIZE: int = Field(default=5, ge=1)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.APP_ENV == "production":
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")

            if not self.DB_PASSWORD.get_secret_value():
                raise ValueError("DB_PASSWORD is required in production")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
