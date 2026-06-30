"""
Reviewer Agent.

Uses LLM to evaluate the final draft against the user request.
"""

import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, NexusState

from nexus.prompts.system_prompts import REVIEWER_PROMPT

logger = structlog.get_logger(__name__)


class ReviewerOutput(BaseModel):
    """Structured output expected from the Reviewer LLM."""
    approved: bool = Field(description="True if the report perfectly answers the query.")
    feedback: str = Field(description="Explanation of approval or specific feedback for revision.")


class ReviewerAgent(BaseAgent):
    """
    Final quality control gate.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.REVIEWER
        
    def execute(self, state: NexusState) -> NexusState:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        
        if not state.draft.content:
            logger.warning("Draft is empty. Sending back to Writer.")
            state.add_error(agent=self.name, message="Draft is missing content.")
            state.current_agent = AgentName.WRITER
            return state

        prompt = ChatPromptTemplate.from_messages([
            ("system", REVIEWER_PROMPT),
            ("user", "User Query: {query}\n\nDraft Report:\n{draft}")
        ])
        
        chain = prompt | self.llm.with_structured_output(ReviewerOutput)
        
        result: ReviewerOutput = chain.invoke({ # type: ignore
            "query": state.user_query,
            "draft": state.draft.content
        })
        
        if result.approved:
            logger.info("Draft approved by Reviewer.")
            state.current_agent = AgentName.SYSTEM
        else:
            logger.warning("Draft rejected by Reviewer.", feedback=result.feedback)
            state.add_error(
                agent=self.name,
                message=f"Draft rejected: {result.feedback}"
            )
            state.current_agent = AgentName.WRITER
            
        return state
