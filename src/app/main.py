import asyncio

from loguru import logger


async def main_async() -> None:
    pass


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在退出...")


if __name__ == "__main__":
    main()
