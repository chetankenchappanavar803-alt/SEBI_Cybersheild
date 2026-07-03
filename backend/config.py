"""
SEBI CyberShield — Configuration Module
Loads all settings from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import os
from pathlib import Path

# Load .env file if present
env_path = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    # ── Gemini ──────────────────────────────────────────────
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    gemini_default_model: str = Field(default="gemini-2.5-flash", env="GEMINI_DEFAULT_MODEL")
    gemini_pro_model: str = Field(default="gemini-2.5-pro", env="GEMINI_PRO_MODEL")
    gemini_timeout: int = Field(default=60, env="GEMINI_TIMEOUT")

    # ── Supabase ─────────────────────────────────────────────
    supabase_url: str = Field(default="", env="SUPABASE_URL")
    supabase_anon_key: str = Field(default="", env="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(default="", env="SUPABASE_SERVICE_ROLE_KEY")
    supabase_jwt_secret: str = Field(default="", env="SUPABASE_JWT_SECRET")

    # ── App ──────────────────────────────────────────────────
    app_env: str = Field(default="development", env="APP_ENV")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    frontend_url: str = Field(default="*", env="FRONTEND_URL")

    # ── Rate Limiting ────────────────────────────────────────
    rate_limit_per_minute: int = Field(default=10, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=100, env="RATE_LIMIT_PER_HOUR")

    # ── Cache ────────────────────────────────────────────────
    cache_ttl: int = Field(default=300, env="CACHE_TTL")

    # ── Upload ───────────────────────────────────────────────
    max_upload_size: int = Field(default=5 * 1024 * 1024, env="MAX_UPLOAD_SIZE")

    # ── HTTP ─────────────────────────────────────────────────
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def gemini_available(self) -> bool:
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")

    @property
    def supabase_available(self) -> bool:
        return bool(
            self.supabase_url
            and self.supabase_url != "https://your-project.supabase.co"
            and self.supabase_anon_key
        )

    model_config = {"env_file": str(env_path), "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
