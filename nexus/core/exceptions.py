"""
Custom exception hierarchy for the Nexus platform.
"""

class NexusError(Exception):
    """Base exception for all Nexus-specific errors."""
    pass


class AgentExecutionError(NexusError):
    """Raised when an agent fails to execute properly."""
    pass


class MaxRetriesExceededError(NexusError):
    """Raised when the Orchestrator loop limit is hit, preventing infinite loops."""
    pass


class StateValidationError(NexusError):
    """Raised when the Shared State becomes invalid or corrupted."""
    pass


class ToolExecutionError(NexusError):
    """Raised when a tool fails to execute safely."""
    pass
