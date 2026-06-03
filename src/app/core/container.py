from functools import cached_property

from langchain_openai import ChatOpenAI

from app.config.enums import ModelProvider
from app.config.settings import settings


class Container:
    """
    DI 容器：负责管理共享实例（如 LLM、数据库等）。
    """

    @cached_property
    def get_llm(self) -> ChatOpenAI:
        if settings.default_model_provider == ModelProvider.OPENAI:
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_api_base,
                model="gpt-4o",
            )
        # 在此处添加更多 Provider
        raise ValueError(f"暂不支持的模型提供商: {settings.default_model_provider}")


container = Container()
