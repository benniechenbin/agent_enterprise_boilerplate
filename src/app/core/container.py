from functools import lru_cache
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from app.config.enums import ModelProvider

class Container:
    """
    DI 容器：负责管理共享实例（如 LLM、数据库等）。
    """
    
    @lru_cache
    def get_llm(self):
        if settings.default_model_provider == ModelProvider.OPENAI:
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_api_base,
                model="gpt-4o",
            )
        # 在此处添加更多 Provider
        raise ValueError(f"暂不支持的模型提供商: {settings.default_model_provider}")

container = Container()
