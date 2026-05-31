import sys
import contextvars
import uuid
from pathlib import Path
from loguru import logger
from app.config.settings import settings

# 1. 定义全局上下文变量
trace_id_var = contextvars.ContextVar("trace_id", default="system")

def setup_logger() -> None:
    """
    配置 loguru 以实现结构化日志，并支持 Trace ID（通过 ContextVars 动态获取）。
    """
    log_dir = settings.resolved_log_dir
    log_dir.mkdir(parents=True, exist_ok=True)

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
        level=settings.log_level,
        colorize=True,
        format=log_format,
    )

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level=settings.log_level,
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | trace_id={extra[trace_id]} | {name}:{line} - {message}",
    )

    # 2. 使用 patcher 动态注入当前上下文的 trace_id
    logger.configure(patcher=lambda record: record["extra"].update(trace_id=trace_id_var.get()))

def set_trace_id(new_id: str = None) -> str:
    """
    设置当前协程/线程的 Trace ID。
    """
    tid = new_id or uuid.uuid4().hex[:8]
    trace_id_var.set(tid)
    return tid

setup_logger()
