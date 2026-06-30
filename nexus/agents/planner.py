"""
Planner Agent.

Uses LLM to decompose user requests into actionable, sequential tasks.
"""

from typing import List
import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, NexusState, ResearchTask, TaskStatus
from nexus.prompts.system_prompts import PLANNER_PROMPT

logger = structlog.get_logger(__name__)


class PlannerOutput(BaseModel):
    """Structured output expected from the Planner LLM."""
    tasks: List[ResearchTask] = Field(description="The sequence of research tasks to execute.")


class PlannerAgent(BaseAgent):
    """
    Decomposes the user query into a structured task graph.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.PLANNER
        
    def execute(self, state: NexusState) -> NexusState:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        
        if not state.plan.tasks:
            logger.info("Generating task decomposition via LLM.")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", PLANNER_PROMPT),
                ("user", "Query: {query}")
            ])
            
            # Use structured output to force the LLM to return our Pydantic model
            chain = prompt | self.llm.with_structured_output(PlannerOutput)
            
            result: PlannerOutput = chain.invoke({"query": state.user_query}) # type: ignore
            
            state.plan.tasks = result.tasks
            state.plan.status = TaskStatus.IN_PROGRESS
            
        # Route to the next agent
        state.current_agent = AgentName.RESEARCHER
        return state
