class AgentApplicationError(RuntimeError):
    """Base error for application-level failures."""


class WorkflowExecutionError(AgentApplicationError):
    """Raised when a workflow cannot complete."""
