"""
Fact Checker Agent.

Uses LLM to validate the evidence gathered by the Researcher.
"""

from typing import List
import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, NexusState

from nexus.prompts.system_prompts import FACT_CHECKER_PROMPT

logger = structlog.get_logger(__name__)


class ValidationResult(BaseModel):
    id: str = Field(description="The ID of the evidence being evaluated.")
    validated: bool = Field(description="True if the evidence is highly credible and logically sound.")
    validation_reason: str = Field(description="Explanation of why it passed or failed.")

class FactCheckerOutput(BaseModel):
    """Structured output expected from the Fact Checker LLM."""
    evaluations: List[ValidationResult]


class FactCheckerAgent(BaseAgent):
    """
    Validates evidence and conditionally routes back to Researcher if issues found.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.FACT_CHECKER
        
    def execute(self, state: NexusState) -> NexusState:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        
        unvalidated_evidence = [e for e in state.evidence if not e.validated]
        
        if not unvalidated_evidence:
            state.current_agent = AgentName.ANALYST
            return state

        logger.info(f"Fact checking {len(unvalidated_evidence)} pieces of evidence.")
        
        evidence_text = "\n".join([f"ID: {e.id} | Claim: {e.content} | Source: {e.source}" for e in unvalidated_evidence])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", FACT_CHECKER_PROMPT),
            ("user", "User Query: {query}\n\nEvidence to evaluate:\n{evidence}")
        ])
        
        chain = prompt | self.llm.with_structured_output(FactCheckerOutput)
        
        result: FactCheckerOutput = chain.invoke({ # type: ignore
            "query": state.user_query,
            "evidence": evidence_text
        })
        
        has_errors = False
        
        # Apply evaluations to state
        for eval_res in result.evaluations:
            # Find the original evidence object
            ev = next((e for e in state.evidence if e.id == eval_res.id), None)
            if ev:
                ev.validated = eval_res.validated
                ev.validation_reason = eval_res.validation_reason
                
                if not ev.validated:
                    has_errors = True
                    state.add_error(
                        agent=self.name,
                        message=f"Evidence {ev.id} failed validation.",
                        context={"source": ev.source, "reason": ev.validation_reason}
                    )
                    logger.warning(f"Evidence {ev.id} rejected: {ev.validation_reason}")

        if has_errors:
            # Loop back to Researcher to fix it
            # In a real system, we'd append a new task to research the rejected claims
            state.current_agent = AgentName.RESEARCHER
        else:
            state.current_agent = AgentName.ANALYST
            
        return state
