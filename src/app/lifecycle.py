from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from app.config.settings import Settings, get_settings
from app.container.container import Container
from app.observability.logger import setup_logger
from app.runtime.runner import AgentRunner
from app.workflows.langgraph_workflow import LangGraphWorkflow


@dataclass(frozen=True, slots=True)
class App:
    container: Container
    runner: AgentRunner


def build_app(app_settings: Settings | None = None) -> App:
    settings = app_settings or get_settings()
    setup_logger(app_settings=settings)
    container = Container.build(app_settings=settings)
    workflow = LangGraphWorkflow(container=container)
    runner = AgentRunner(workflow=workflow, container=container)
    return App(container=container, runner=runner)


@asynccontextmanager
async def lifespan(app_settings: Settings | None = None) -> AsyncGenerator[App, None]:
    app = build_app(app_settings=app_settings)
    try:
        yield app
    finally:
        pass
