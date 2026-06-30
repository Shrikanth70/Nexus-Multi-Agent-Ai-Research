"""Core domain models and interfaces for Nexus."""

from .state import (
    AgentName,
    DraftReport,
    ErrorRecord,
    Evidence,
    NexusState,
    ResearchTask,
    TaskGraph,
    TaskStatus,
)
from .exceptions import (
    NexusError,
    AgentExecutionError,
    MaxRetriesExceededError,
    StateValidationError,
    ToolExecutionError,
)

__all__ = [
    "AgentName",
    "DraftReport",
    "ErrorRecord",
    "Evidence",
    "NexusState",
    "ResearchTask",
    "TaskGraph",
    "TaskStatus",
    "NexusError",
    "AgentExecutionError",
    "MaxRetriesExceededError",
    "StateValidationError",
    "ToolExecutionError",
]
