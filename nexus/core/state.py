"""
Core Nexus State definitions.

This module defines the strictly-typed Shared State schemas using Pydantic.
Per STATE.md, all communication between agents occurs through these typed objects.
No hidden string prompts or untyped dictionaries are allowed.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    """Standardized output contract for all agents."""
    agent: str = Field(..., description="The name of the agent that produced this output.")
    status: str = Field(..., description="Status of the agent execution (e.g., 'success', 'error').")
    data: Dict[str, Any] = Field(default_factory=dict, description="The specific mutations to apply to the state.")
    logs: List[str] = Field(default_factory=list, description="Execution logs from the agent.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentName(str, Enum):
    """Enumeration of all valid agents in the system."""
    PLANNER = "Planner"
    RESEARCHER = "Researcher"
    FACT_CHECKER = "FactChecker"
    ANALYST = "Analyst"
    WRITER = "Writer"
    REVIEWER = "Reviewer"
    # Used when the workflow is complete or paused
    SYSTEM = "System"


class TaskStatus(str, Enum):
    """Status of an individual research task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchTask(BaseModel):
    """A single sub-task decomposed from the main user query by the Planner."""
    id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    description: str = Field(..., description="A clear, actionable description of what to research.")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    result: Optional[str] = Field(default=None, description="The raw findings/summary from the Researcher.")
    assigned_to: Optional[AgentName] = Field(default=None)


class TaskGraph(BaseModel):
    """The complete execution plan."""
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    tasks: List[ResearchTask] = Field(default_factory=list)


class Evidence(BaseModel):
    """A single piece of validated factual information."""
    id: str = Field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:8]}")
    task_id: str = Field(..., description="The ID of the task that generated this evidence.")
    content: str = Field(..., description="The actual factual claim or data point.")
    source: str = Field(..., description="URL, document ID, or citation where this was found.")
    validated: bool = Field(default=False, description="True if the Fact Checker approved it.")
    validation_reason: Optional[str] = Field(default=None, description="Why it was approved or rejected.")


class DraftReport(BaseModel):
    """The synthesized research report."""
    content: Optional[str] = Field(default=None)
    revisions: int = Field(default=0)


class ErrorRecord(BaseModel):
    """Tracks failures to prevent infinite loops and provide feedback."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_name: AgentName
    error_message: str
    context: Dict[str, Any] = Field(default_factory=dict)


class NexusState(BaseModel):
    """
    The Shared State Object — The single source of truth for the entire workflow.
    
    This object is passed to every agent. Agents read from it, execute their logic,
    and return a mutated copy of it.
    """
    session_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:8]}")
    user_query: str = Field(..., description="The original research request from the user.")
    
    # State tracking
    current_agent: AgentName = Field(default=AgentName.PLANNER)
    retry_count: int = Field(default=0, description="Tracks loops to prevent infinite loops.")
    is_paused_for_human: bool = Field(default=False, description="True if HITL intervention is needed.")
    
    # Payload
    plan: TaskGraph = Field(default_factory=TaskGraph)
    evidence: List[Evidence] = Field(default_factory=list)
    analysis_notes: List[str] = Field(default_factory=list, description="Synthesis points from the Analyst.")
    draft: DraftReport = Field(default_factory=DraftReport)
    errors: List[ErrorRecord] = Field(default_factory=list)

    def add_error(self, agent: AgentName, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Helper to safely append an error and increment retry count."""
        self.errors.append(ErrorRecord(
            agent_name=agent,
            error_message=message,
            context=context or {}
        ))
        self.retry_count += 1
