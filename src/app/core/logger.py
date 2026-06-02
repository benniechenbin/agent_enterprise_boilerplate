import sys
import contextvars
import uuid
from collections.abc import Callable
from pathlib import Path
from loguru import logger
from app.config.settings import settings

# 1. 定义全局上下文变量
trace_id_var = contextvars.ContextVar("trace_id", default="system")

def setup_logger(
    log_dir: Path | None = None,
    log_level: str | None = None,
    log_file_name: str = "system_{time:YYYY-MM-DD}.log",
) -> Path:
    """
    配置 loguru 以实现结构化日志，并支持 Trace ID（通过 ContextVars 动态获取）。
    """
    target_dir = log_dir or settings.resolved_log_dir
    target_level = log_level or settings.log_level
    target_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()

    # 标准格式，使用 {extra[trace_id]} 占位符
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
        colorize=True,
        format=log_format,
    )

    logger.add(
        target_dir / log_file_name,
        rotation="00:00",
        retention="30 days",
        level=target_level,
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | trace_id={extra[trace_id]} | {name}:{line} - {message}",
    )

    # 2. 使用 patcher 动态注入当前上下文的 trace_id
    logger.configure(patcher=lambda record: record["extra"].update(trace_id=trace_id_var.get()))

    return target_dir

def set_trace_id(new_id: str = None) -> str:
    """
    设置当前协程/线程的 Trace ID。
    """
    tid = new_id or uuid.uuid4().hex[:8]
    trace_id_var.set(tid)
    return tid

def add_custom_file(
    file_name: str,
    log_dir: Path | None = None,
    level: str = "INFO",
    filter_rule: str | Callable | None = None,
) -> int:
    """
    运行时添加一个额外的文件日志输出，并返回对应的 handler id。
    """
    target_dir = log_dir or settings.resolved_log_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    handler_id = logger.add(
        target_dir / file_name,
        level=level,
        rotation="10 MB",
        filter=filter_rule,
    )
    return handler_id

setup_logger()
