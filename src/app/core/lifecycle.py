from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from app.config.settings import settings
from app.core.banner import show_banner
from app.core.container import Container, container
from app.core.logger import logger


class AppLifecycle:
    """
    管理应用程序资源的预热和优雅停机。
    """

    def __init__(self, app_container: Container | None = None) -> None:
        self.container = app_container or container
        self._resources: list[Any] = []

    async def on_startup(self) -> None:
        show_banner(text=settings.app_name, font="slant")
        logger.info("正在初始化应用程序资源...")
        self.container.validate()
        logger.info("应用程序启动完成。")

    async def on_shutdown(self) -> None:
        logger.info("正在关闭应用程序资源...")
        # 在此处添加资源清理逻辑
        logger.info("应用程序停机完成。")


lifecycle = AppLifecycle()


@asynccontextmanager
async def lifespan() -> AsyncGenerator[None, None]:
    """
    管理应用程序生命周期的上下文管理器。
    """
    try:
        await lifecycle.on_startup()
        yield
    finally:
        await lifecycle.on_shutdown()
