from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

@lru_cache
def get_database_settings() -> "DataBaseSettings":
    return DataBaseSettings()

class DataBaseSettings(BaseSettings):
    db_url: str = Field(default="sqlite+aiosqlite:///db.sqlite", alias="DB_URL")
    
    model_config = SettingsConfigDict(
        env_file="database_settings.env",
        env_file_encoding="utf-8",
    )