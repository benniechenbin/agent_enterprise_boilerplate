import asyncio

from app.core.lifecycle import lifecycle
from app.main import main_async


def test_main_async_runs_lifecycle(monkeypatch) -> None:
    events: list[str] = []

    async def on_startup() -> None:
        events.append("startup")

    async def on_shutdown() -> None:
        events.append("shutdown")

    monkeypatch.setattr(lifecycle, "on_startup", on_startup)
    monkeypatch.setattr(lifecycle, "on_shutdown", on_shutdown)

    asyncio.run(main_async())

    assert events == ["startup", "shutdown"]
