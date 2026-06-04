from typing import Any, Protocol


class Tracer(Protocol):
    """Extension point for a future tracing implementation."""

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None: ...
