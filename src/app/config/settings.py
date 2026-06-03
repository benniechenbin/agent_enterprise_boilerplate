from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.enums import AppEnv, ModelProvider


def find_project_root(
    current_path: Path, markers: tuple[str, ...] = ("pyproject.toml", "requirements.txt", ".git")
) -> Path:
    for parent in current_path.parents:
        if any((parent / marker).exists() for marker in markers):
            return parent
    return current_path.parent


BASE_DIR = find_project_root(Path(__file__).resolve())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # 项目配置
    app_name: str = "agent-enterprise-boilerplate"
    app_env: AppEnv = AppEnv.DEV

    # 日志配置
    log_dir: Path = Path("logs")
    log_level: str = "INFO"

    # LLM 配置
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

    # 工具配置
    tavily_api_key: SecretStr | None = None

    @property
    def resolved_log_dir(self) -> Path:
        """
        获取解析后的绝对日志目录路径。
        """
        if self.log_dir.is_absolute():
            return self.log_dir
        return BASE_DIR / self.log_dir

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


settings = get_settings()
