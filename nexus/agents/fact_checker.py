"""
Fact Checker Agent.

Uses LLM to validate the evidence gathered by the Researcher.
"""

from typing import List
import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import (
    AgentName,
    NexusState,
    AgentOutput,
    ErrorRecord,
    ResearchTask,
    TaskStatus,
)
from nexus.config import settings

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
        
    def execute(self, state: NexusState) -> AgentOutput:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        logs = []
        
        unvalidated_evidence = [e for e in state.evidence if e.validation_reason is None]
        
        if not unvalidated_evidence:
            valid_evidence = [e for e in state.evidence if e.validated]
            if valid_evidence or state.retry_count >= settings.nexus_max_retry_count:
                state.current_agent = AgentName.ANALYST
                logs.append("No unvalidated evidence found. Routing to Analyst.")
            else:
                state.retry_count += 1
                state.plan.tasks.append(
                    ResearchTask(
                        description=f"Gather reliable and credible evidence for: {state.user_query}",
                        status=TaskStatus.PENDING,
                    )
                )
                state.current_agent = AgentName.RESEARCHER
                logs.append("No valid evidence found. Routing back to Researcher.")
            return AgentOutput(
                agent=self.name.value,
                status="success",
                data=state.model_dump(),
                logs=logs
            )

        logger.info(f"Fact checking {len(unvalidated_evidence)} pieces of evidence.")
        logs.append(f"Fact checking {len(unvalidated_evidence)} pieces of evidence.")
        
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
        
        # Apply evaluations to state
        for eval_res in result.evaluations:
            # Find the original evidence object
            ev = next((e for e in state.evidence if e.id == eval_res.id), None)
            if ev:
                ev.validated = eval_res.validated
                ev.validation_reason = eval_res.validation_reason
                
                if not ev.validated:
                    state.errors.append(
                        ErrorRecord(
                            agent_name=self.name,
                            error_message=f"Evidence {ev.id} failed validation.",
                            context={"source": ev.source, "reason": ev.validation_reason}
                        )
                    )
                    logger.warning(f"Evidence {ev.id} rejected: {ev.validation_reason}")

        valid_evidence = [e for e in state.evidence if e.validated]
        if valid_evidence:
            state.current_agent = AgentName.ANALYST
            logs.append("Validated evidence available. Routing to Analyst.")
        elif state.retry_count < settings.nexus_max_retry_count:
            state.retry_count += 1
            state.plan.tasks.append(
                ResearchTask(
                    description=f"Gather reliable and credible evidence for: {state.user_query}",
                    status=TaskStatus.PENDING,
                )
            )
            state.current_agent = AgentName.RESEARCHER
            logs.append("All evidence failed validation. Routing back to Researcher with new task.")
        else:
            state.current_agent = AgentName.ANALYST
            logs.append("Max retries reached. Routing to Analyst with available evidence.")
            
        return AgentOutput(
            agent=self.name.value,
            status="success",
            data=state.model_dump(),
            logs=logs
        )
