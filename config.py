from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    environment: str = "development"

    # Get a Gemini API key from Google AI Studio and place it in .env.
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    # Optional local concept-explanation model from the project specification.
    # Disabled by default because the model is large and downloads on first use.
    local_explanation_enabled: bool = False
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"

    max_input_chars: int = 12000
    request_timeout_seconds: int = 90

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
