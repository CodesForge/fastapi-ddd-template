from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

@lru_cache
def get_rabbit_settings() -> "RabbitSettings":
    return RabbitSettings()

class RabbitSettings(BaseSettings):
    rabbit_url: str = Field(default="amqp://guest:guest@rabbit:5672/", alias="RABBIT_URL")
    
    model_config = SettingsConfigDict(
        env_file="rabbit_settings.env",
        env_file_encoding="utf-8",
    )