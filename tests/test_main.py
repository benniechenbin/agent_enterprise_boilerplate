import asyncio
from dataclasses import dataclass
from typing import Any

from app import main as main_module


def test_main_async_delegates_to_runner(monkeypatch) -> None:
    inputs: list[str] = []

    class StubRunner:
        async def arun(self, input_data: str) -> dict[str, Any]:
            inputs.append(input_data)
            return {"status": "completed"}

    @dataclass
    class StubApp:
        runner: StubRunner

    monkeypatch.setattr(main_module, "build_app", lambda: StubApp(runner=StubRunner()))

    asyncio.run(main_module.main_async())

    assert inputs == ["Create a simple plan."]
