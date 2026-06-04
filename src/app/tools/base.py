from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name."""

    @abstractmethod
    async def arun(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the tool."""
