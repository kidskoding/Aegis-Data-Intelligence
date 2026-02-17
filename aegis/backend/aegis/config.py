"""Application configuration from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "AEGIS_"}

    # API
    api_key: str = "dev-key"

    # Database
    db_path: str = str(Path("data/aegis.db"))

    # Scheduling
    scan_interval_seconds: int = 300
    lineage_refresh_seconds: int = 3600
    rediscovery_interval_seconds: int = 86400  # 24 hours

    # Logging
    log_level: str = "INFO"

    # Encryption
    encryption_key: str = ""

    # OpenAI (no prefix — uses OPENAI_API_KEY directly)
    openai_api_key: str = ""

    model_config = {
        "env_prefix": "AEGIS_",
        "env_file": ".env",
        "extra": "ignore",
    }

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    @property
    def sync_database_url(self) -> str:
        return f"sqlite:///{self.db_path}"


settings = Settings()
