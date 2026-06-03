from loguru import logger


def test_setup_logger_initializes() -> None:
    # Logger is already setup on import of app.core.logger
    # We just verify it can log without error
    logger.info("test message")
    logger.configure(extra={"trace_id": "test"})
    logger.info("test message with trace_id")
