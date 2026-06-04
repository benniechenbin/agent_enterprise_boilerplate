from typing import Any

from app.tools.base import BaseTool


class SearchTool(BaseTool):
    """Placeholder for a project-specific search implementation."""

    @property
    def name(self) -> str:
        return "search"

    async def arun(self, input_data: dict[str, Any]) -> dict[str, Any]:
        del input_data
        raise NotImplementedError("Configure a search provider before using SearchTool.")
