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

    app_name: str = Field(
        default="agent-enterprise-boilerplate",
        description="Application name used in logs and runtime metadata.",
    )
    app_env: AppEnv = Field(
        default=AppEnv.DEV,
        description="Runtime environment: development, testing, or production.",
    )

    log_dir: Path = Field(
        default=Path("logs"),
        description="Log directory. Relative paths resolve from the working directory.",
    )
    log_level: str = Field(
        default="INFO",
        description="Log level such as DEBUG, INFO, WARNING, ERROR, or CRITICAL.",
    )

    default_model_provider: ModelProvider = Field(
        default=ModelProvider.OPENAI,
        description="Default model provider.",
    )
    model_name: str = Field(
        default="gpt-4o-mini",
        description="Default model name.",
    )
    openai_api_key: SecretStr | None = Field(
        default=None,
        description="OpenAI API key.",
    )
    openai_api_base: str | None = Field(
        default=None,
        description="Optional OpenAI-compatible API base URL.",
    )

    anthropic_api_key: SecretStr | None = Field(
        default=None,
        description="Anthropic API key.",
    )
    google_api_key: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        description="Google or Gemini API key. GOOGLE_API_KEY is the preferred name.",
    )
    deepseek_api_key: SecretStr | None = Field(
        default=None,
        description="DeepSeek API key.",
    )
    tavily_api_key: SecretStr | None = Field(
        default=None,
        description="Tavily API key used by an optional search integration.",
    )

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
