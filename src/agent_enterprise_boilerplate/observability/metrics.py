from typing import Protocol


class Metrics(Protocol):
    """Extension point for a future metrics implementation."""

    def increment(self, name: str, value: int = 1) -> None: ...
