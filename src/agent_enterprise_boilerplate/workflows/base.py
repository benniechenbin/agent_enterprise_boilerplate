from abc import ABC, abstractmethod
from typing import Any

from agent_enterprise_boilerplate.runtime.context import RunContext


class BaseWorkflow(ABC):
    @abstractmethod
    async def arun(
        self,
        input_data: dict[str, Any],
        context: RunContext,
    ) -> dict[str, Any]:
        """Execute the workflow for one run."""
