from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from app.config.enums import AppEnv, ModelProvider

def find_project_root(current_path: Path, markers: tuple = ("pyproject.toml", "requirements.txt", ".git")) -> Path:   
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
    )

    # 项目配置
    app_name: str = "agent-enterprise-boilerplate"
    app_env: AppEnv = AppEnv.DEV

    # 日志配置
    log_dir: Path = Path("logs")
    log_level: str = "INFO"

    # LLM 配置
    default_model_provider: ModelProvider = ModelProvider.OPENAI
    openai_api_key: Optional[str] = None
    openai_api_base: Optional[str] = None
    
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None

    # 工具配置
    tavily_api_key: Optional[str] = None

    @property
    def resolved_log_dir(self) -> Path:
        """
        获取解析后的绝对日志目录路径。
        """
        if self.log_dir.is_absolute():
            return self.log_dir
        return BASE_DIR / self.log_dir


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
