from contextlib import asynccontextmanager
from loguru import logger

class AppLifecycle:
    """
    管理应用程序资源的预热和优雅停机。
    """
    def __init__(self):
        self._resources = []

    async def on_startup(self):
        logger.info("正在初始化应用程序资源...")
        # 在此处添加资源初始化逻辑（例如：数据库连接池、LLM 预热）
        logger.info("应用程序启动完成。")

    async def on_shutdown(self):
        logger.info("正在关闭应用程序资源...")
        # 在此处添加资源清理逻辑
        logger.info("应用程序停机完成。")

lifecycle = AppLifecycle()

@asynccontextmanager
async def lifespan():
    """
    管理应用程序生命周期的上下文管理器。
    """
    try:
        await lifecycle.on_startup()
        yield
    finally:
        await lifecycle.on_shutdown()
