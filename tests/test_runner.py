import asyncio
from pathlib import Path

from app.config.enums import AppEnv
from app.config.settings import Settings
from app.lifecycle import App, build_app


def make_test_app(tmp_path: Path) -> App:
    settings = Settings(_env_file=None, app_env=AppEnv.TEST, log_dir=tmp_path)
    return build_app(app_settings=settings)


def test_build_app_creates_runner(tmp_path: Path) -> None:
    app = make_test_app(tmp_path)

    assert app.container is not None
    assert app.runner is not None


def test_runner_execution_returns_unified_result(tmp_path: Path) -> None:
    app = make_test_app(tmp_path)

    result = asyncio.run(app.runner.arun("test"))

    assert isinstance(result, dict)
    assert result["request_id"]
    assert result["status"] == "completed"
    assert result["result"]["output"]["status"] == "completed"
