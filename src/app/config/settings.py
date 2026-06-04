from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.enums import AppEnv, ModelProvider


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = "agent-enterprise-boilerplate"
    app_env: AppEnv = AppEnv.DEV

    log_dir: Path = Path("logs")
    log_level: str = "INFO"

    default_model_provider: ModelProvider = ModelProvider.OPENAI
    model_name: str = "gpt-4o-mini"
    openai_api_key: SecretStr | None = None
    openai_api_base: str | None = None

    anthropic_api_key: SecretStr | None = None
    google_api_key: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("GOOGLE_API_KEY", "GEMINI_API_KEY"),
    )
    deepseek_api_key: SecretStr | None = None
    tavily_api_key: SecretStr | None = None

    @property
    def resolved_log_dir(self) -> Path:
        if self.log_dir.is_absolute():
            return self.log_dir
        return Path.cwd() / self.log_dir

    def require_provider_credentials(self, provider: ModelProvider | None = None) -> None:
        selected_provider = provider or self.default_model_provider
        provider_keys: dict[ModelProvider, tuple[SecretStr | None, str]] = {
            ModelProvider.OPENAI: (self.openai_api_key, "OPENAI_API_KEY"),
            ModelProvider.ANTHROPIC: (self.anthropic_api_key, "ANTHROPIC_API_KEY"),
            ModelProvider.GOOGLE: (self.google_api_key, "GOOGLE_API_KEY"),
            ModelProvider.DEEPSEEK: (self.deepseek_api_key, "DEEPSEEK_API_KEY"),
        }
        api_key, env_name = provider_keys[selected_provider]
        if api_key is None or not api_key.get_secret_value():
            raise ValueError(f"{selected_provider.value} provider requires {env_name}.")


@lru_cache
def get_settings() -> Settings:
    return Settings()
