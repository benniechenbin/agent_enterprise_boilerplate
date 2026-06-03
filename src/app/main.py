import asyncio

from loguru import logger

from app.core.lifecycle import lifespan


async def main_async() -> None:
    async with lifespan():
        logger.info("应用启动链路验证完成。")


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在退出...")


if __name__ == "__main__":
    main()
