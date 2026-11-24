"""Application settings, read from environment variables and an optional .env file.

This is the one place where configuration enters the backend. Secrets such as
API keys (added in later phases) also arrive here and are never logged.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Browser origins allowed to call this API, separated by commas.
    # Development default: the Vite dev server. In production the host sets the
    # frontend's real address through an environment variable (TD-014).
    cors_allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        """The allowed origins as a clean list (spaces and blank entries removed)."""
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Create the settings once and reuse them."""
    return Settings()