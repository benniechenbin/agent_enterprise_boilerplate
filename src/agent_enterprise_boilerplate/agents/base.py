from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Extension point for agent capabilities that outgrow workflow nodes."""

    @abstractmethod
    async def arun(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute one agent capability."""
