"""
Writer Agent.

Uses LLM to draft the final report in Markdown.
"""

import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, NexusState, AgentOutput

from nexus.prompts.system_prompts import WRITER_PROMPT

logger = structlog.get_logger(__name__)


class WriterOutput(BaseModel):
    """Structured output expected from the Writer LLM."""
    draft_markdown: str = Field(description="The full drafted report in Markdown format.")


class WriterAgent(BaseAgent):
    """
    Drafts the final report based on analysis notes.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.WRITER
        
    def execute(self, state: NexusState) -> AgentOutput:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        logs = []
        
        if not state.analysis_notes:
            logger.warning("No analysis notes available to write about.")
            logs.append("No analysis notes available to write about.")
            
        notes_text = "\n".join([f"- {note}" for note in state.analysis_notes])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", WRITER_PROMPT),
            ("user", "User Query: {query}\n\nAnalysis Notes:\n{notes}")
        ])
        
        # We can use structured output to ensure we just get the markdown string and no conversational filler.
        chain = prompt | self.llm.with_structured_output(WriterOutput)
        
        result: WriterOutput = chain.invoke({ # type: ignore
            "query": state.user_query,
            "notes": notes_text
        })
        
        state.draft.content = result.draft_markdown
        state.draft.revisions += 1
        
        state.current_agent = AgentName.REVIEWER
        logs.append(f"Draft written (revision {state.draft.revisions}).")
        return AgentOutput(
            agent=self.name.value,
            status="success",
            data=state.model_dump(),
            logs=logs
        )
