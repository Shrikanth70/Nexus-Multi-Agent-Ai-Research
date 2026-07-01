import structlog
from pydantic import BaseModel, Field
from typing import List, Optional

# Assuming BaseAgent or simple LLM init is possible, but we'll use langchain directly for the judge
from langchain_core.prompts import ChatPromptTemplate
# we can use the same llm setup as agents, or just use Ollama/OpenAI directly.
# For simplicity, we'll try to use the configured LLM if available, otherwise just define the schema.

logger = structlog.get_logger(__name__)

class EvaluationCriteria(BaseModel):
    criteria_name: str
    score: int = Field(ge=1, le=5, description="Score from 1 to 5")
    reasoning: str = Field(description="Explanation for the score")

class EvaluationResult(BaseModel):
    is_passing: bool = Field(description="True if the report meets the overall standard.")
    total_score: int
    criteria_scores: List[EvaluationCriteria]
    constructive_feedback: str

JUDGE_PROMPT = """
You are an expert evaluator. Your job is to assess an AI-generated research report against the original user query.

Original Query: {query}

Generated Report:
{report}

Evaluate the report on the following criteria (1-5 each):
1. Factuality: Does the report rely on provided evidence or does it hallucinate?
2. Completeness: Does it fully answer the original query?
3. Formatting: Is it well-structured and easy to read?

Output your evaluation strictly in the requested format.
"""

def evaluate_report(llm, query: str, report_content: str) -> EvaluationResult:
    """Uses LLM-as-a-judge to evaluate a generated report."""
    logger.info("Evaluating report using LLM judge...")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an impartial, strict evaluator."),
        ("user", JUDGE_PROMPT)
    ])
    
    chain = prompt | llm.with_structured_output(EvaluationResult)
    result: EvaluationResult = chain.invoke({
        "query": query,
        "report": report_content
    })
    
    return result
