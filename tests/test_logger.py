from pathlib import Path

from loguru import logger

from app.core.logger import set_trace_id, setup_logger


def test_setup_logger_creates_log_dir(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"

    resolved_dir = setup_logger(log_dir=log_dir, log_level="INFO")

    assert resolved_dir == log_dir
    assert log_dir.exists()


def test_logger_accepts_trace_id(tmp_path: Path) -> None:
    setup_logger(log_dir=tmp_path, log_level="INFO")
    set_trace_id("test-trace")

    logger.info("test message")
