"""
Base interface for all Nexus Agents.

Per AGENTS.md, agents are stateless pure functions with respect to the orchestrator.
They take a NexusState, execute their specialized logic, and return a mutated NexusState.
"""

from abc import ABC, abstractmethod
import structlog

from nexus.core.state import AgentName, NexusState

logger = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents.
    
    In Phase 2, agents utilize a LangChain ChatModel to reason over the State.
    """
    
    def __init__(self) -> None:
        """Initialize the agent and its LLM connection."""
        from nexus.llm.provider import get_llm
        self.llm = get_llm()
    
    @property
    @abstractmethod
    def name(self) -> AgentName:
        """The unique identifier for this agent."""
        pass
        
    @abstractmethod
    def execute(self, state: NexusState) -> NexusState:
        """
        The core agent logic.
        
        Args:
            state: The current Shared State.
            
        Returns:
            The mutated Shared State.
        """
        pass
