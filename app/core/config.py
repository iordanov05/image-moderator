from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    deepai_api_key: str = Field(..., alias="DEEPAI_API_KEY")
    nsfw_threshold: float = Field(0.7, alias="NSFW_THRESHOLD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,  
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
