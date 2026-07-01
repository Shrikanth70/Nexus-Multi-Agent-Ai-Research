import pytest
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda

from nexus.evaluation.llm_judge import evaluate_report

# Mock LLM for testing
def mock_chain_invoke(inputs):
    from nexus.evaluation.llm_judge import EvaluationResult, EvaluationCriteria
    return EvaluationResult(
        is_passing=True,
        total_score=15,
        criteria_scores=[
            EvaluationCriteria(criteria_name="Factuality", score=5, reasoning="Good"),
            EvaluationCriteria(criteria_name="Completeness", score=5, reasoning="Good"),
            EvaluationCriteria(criteria_name="Formatting", score=5, reasoning="Good"),
        ],
        constructive_feedback="Excellent job."
    )

class MockLLM:
    def with_structured_output(self, schema):
        return RunnableLambda(mock_chain_invoke)

@pytest.mark.unit
def test_evaluate_report():
    llm = MockLLM()
    result = evaluate_report(llm, "What is AI?", "AI is artificial intelligence.")
    
    assert result.is_passing is True
    assert result.total_score == 15
    assert len(result.criteria_scores) == 3
