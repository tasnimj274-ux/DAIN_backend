from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration loaded from environment variables and an optional .env file."""

    database_url: str
    institutional_email_domain: str
    app_env: str = "development"
    debug: bool = False
    
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    email_from: str | None = None
    brevo_api_key: str | None = None
    smtp_use_ssl: bool = False
    verification_token_ttl_minutes: int = 60
    session_token_ttl_minutes: int = 1440
    expose_verification_token_in_response: bool = False
    media_root: str = "uploads"
    max_upload_size_bytes: int = 5_242_880
    cors_origins: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
