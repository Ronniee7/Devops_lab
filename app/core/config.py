from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded from Environment Variables
    or the local .env file.
    """

    APP_NAME: str =  "Devops Lab API" 
    APP_VERSION: str = "0.2.0"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    DEBUG: bool = True

model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
)


settings = Settings()
