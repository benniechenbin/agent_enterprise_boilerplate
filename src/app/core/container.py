from functools import cached_property
from typing import Any

from app.config.enums import ModelProvider
from app.config.settings import Settings, settings


class Container:
    """
    DI 容器：负责管理共享实例（如 LLM、数据库等）。
    """

    def __init__(self, app_settings: Settings | None = None) -> None:
        self.settings = app_settings or settings

    def validate(self) -> None:
        self.settings.require_provider_credentials()
        if self.settings.default_model_provider != ModelProvider.OPENAI:
            raise ValueError(f"暂不支持的模型提供商: {self.settings.default_model_provider}")

    @cached_property
    def llm(self) -> Any:
        if self.settings.default_model_provider == ModelProvider.OPENAI:
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:
                raise RuntimeError("请先安装 langchain-openai 依赖。") from exc

            return ChatOpenAI(
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_api_base,
                model=self.settings.model_name,
            )
        # 在此处添加更多 Provider
        raise ValueError(f"暂不支持的模型提供商: {self.settings.default_model_provider}")


container = Container()
