import contextvars
import sys
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from loguru import logger as logger

from agent_enterprise_boilerplate.config.enums import AppEnv
from agent_enterprise_boilerplate.config.settings import get_settings

trace_id_var = contextvars.ContextVar("trace_id", default="system")


def setup_logger(
    log_dir: Path | None = None,
    log_level: str | None = None,
    log_prefix: str = "system",
) -> Path:
    settings = get_settings()
    target_dir = log_dir or settings.resolved_log_dir
    target_level = log_level or settings.log_level
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file_name = f"{log_prefix}_{{time:YYYY-MM-DD}}.log"
    is_development = settings.app_env == AppEnv.DEV

    logger.remove()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<magenta>trace_id={extra[trace_id]}</magenta> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(
        sys.stdout,
        level=target_level,
        colorize=is_development,
        format=log_format,
    )
    logger.add(
        target_dir / log_file_name,
        rotation="00:00",
        retention="30 days",
        level=target_level,
        enqueue=True,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "trace_id={extra[trace_id]} | {name}:{line} - {message}"
        ),
    )
    logger.configure(patcher=lambda record: record["extra"].update(trace_id=trace_id_var.get()))
    return target_dir


def set_trace_id(new_id: str | None = None) -> str:
    trace_id = new_id or uuid.uuid4().hex
    trace_id_var.set(trace_id)
    return trace_id


def get_trace_id() -> str:
    return trace_id_var.get()


def add_custom_file(
    file_name: str,
    log_dir: Path | None = None,
    level: str = "INFO",
    filter_rule: str | Callable[..., Any] | None = None,
) -> int:
    settings = get_settings()
    target_dir = log_dir or settings.resolved_log_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    return logger.add(
        target_dir / file_name,
        level=level,
        rotation="10 MB",
        filter=filter_rule,
    )
