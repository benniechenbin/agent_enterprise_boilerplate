import asyncio

from loguru import logger

from app.core.constants import DEFAULT_RUN_INPUT
from app.lifecycle import build_app


async def main_async() -> None:
    app = build_app()
    result = await app.runner.arun(DEFAULT_RUN_INPUT)
    logger.info("Agent run completed: {}", result)


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Application interrupted.")


if __name__ == "__main__":
    main()
