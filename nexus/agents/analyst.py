"""
Analyst Agent.

Uses LLM to synthesize patterns and insights from validated evidence.
"""

from typing import List
import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, NexusState, AgentOutput

from nexus.prompts.system_prompts import ANALYST_PROMPT

logger = structlog.get_logger(__name__)


class AnalystOutput(BaseModel):
    """Structured output expected from the Analyst LLM."""
    notes: List[str] = Field(description="List of analytical insights and synthesized points.")


class AnalystAgent(BaseAgent):
    """
    Synthesizes validated evidence into analysis notes.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.ANALYST
        
    def execute(self, state: NexusState) -> AgentOutput:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        logs = []
        
        valid_evidence = [e for e in state.evidence if e.validated]
        
        if not valid_evidence:
            logger.warning("No valid evidence available to analyze.")
            state.current_agent = AgentName.WRITER
            logs.append("No valid evidence available to analyze.")
            return AgentOutput(
                agent=self.name.value,
                status="success",
                data=state.model_dump(),
                logs=logs
            )

        logger.info(f"Analyzing {len(valid_evidence)} pieces of valid evidence.")
        logs.append(f"Analyzing {len(valid_evidence)} pieces of valid evidence.")
        
        evidence_text = "\n".join([f"- {e.content}" for e in valid_evidence])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", ANALYST_PROMPT),
            ("user", "User Query: {query}\n\nValidated Evidence:\n{evidence}")
        ])
        
        chain = prompt | self.llm.with_structured_output(AnalystOutput)
        
        result: AnalystOutput = chain.invoke({ # type: ignore
            "query": state.user_query,
            "evidence": evidence_text
        })
        
        state.analysis_notes = result.notes
        
        state.current_agent = AgentName.WRITER
        logs.append(f"Generated {len(result.notes)} analysis notes.")
        return AgentOutput(
            agent=self.name.value,
            status="success",
            data=state.model_dump(),
            logs=logs
        )
