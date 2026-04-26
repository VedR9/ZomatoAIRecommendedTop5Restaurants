from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = "development"
    app_name: str = "Restaurant Recommendation System"
    app_port: int = 8000
    log_level: str = "INFO"
    llm_api_key: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
