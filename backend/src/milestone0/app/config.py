from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "Restaurant Recommendation System"
    app_port: int = 8000
    log_level: str = "INFO"
    llm_api_key: str | None = None
    gemini_api_key: str | None = None
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    dataset_limit: int | None = None  # set to e.g. 3000 on free-tier hosts


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
