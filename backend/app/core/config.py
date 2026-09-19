from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Darukaa.Earth'
    database_url: str = 'sqlite:///./darukaa.db'
    jwt_secret_key: str = 'change-me-in-production'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    mapbox_access_token: str = 'demo-token'
    ai_api_key: str = 'demo-key'
    ai_model: str = 'gpt-4o-mini'
    cors_origins: List[str] = ['http://localhost:5173']

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
