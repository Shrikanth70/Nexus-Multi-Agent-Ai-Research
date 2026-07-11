"""Tests for individual agents using mocked LLMs."""

import pytest
from unittest.mock import patch, MagicMock

from nexus.core.state import AgentName, Evidence, NexusState, ResearchTask, TaskStatus
from nexus.agents.planner import PlannerAgent, PlannerOutput
from nexus.agents.researcher import ResearcherAgent, FindingsOutput, SearchQueryOutput
from nexus.agents.fact_checker import FactCheckerAgent, FactCheckerOutput, ValidationResult

@pytest.fixture
def mock_chain_invoke():
    """Mocks the LangChain RunnableSequence.invoke method to bypass LLM calls."""
    with patch("langchain_core.runnables.RunnableSequence.invoke") as mock_invoke:
        yield mock_invoke

@pytest.fixture
def mock_tools():
    """Mocks the external tools for ResearcherAgent."""
    with patch("nexus.agents.researcher.web_search") as m_search, \
         patch("nexus.agents.researcher.scrape_url") as m_scrape, \
         patch("nexus.agents.researcher.vector_memory") as m_vector:
        
        m_search.return_value = [{"title": "Test", "link": "http://test.com", "snippet": "Test snippet"}]
        m_scrape.return_value = "Mock extracted content"
        m_vector.search_documents.return_value = [{"text": "Mock context", "metadata": {"url": "http://test.com"}}]
        
        yield m_search, m_scrape, m_vector


@pytest.mark.unit
def test_planner_agent(mock_chain_invoke) -> None:
    state = NexusState(user_query="Test")
    agent = PlannerAgent()
    
    # Setup mock return
    mock_chain_invoke.return_value = PlannerOutput(
        tasks=[
            ResearchTask(description="Mock Task 1", status=TaskStatus.PENDING),
            ResearchTask(description="Mock Task 2", status=TaskStatus.PENDING)
        ]
    )
    
    output = agent.execute(state)
    
    assert output.status == "success"
    assert state.current_agent == AgentName.RESEARCHER
    assert len(state.plan.tasks) == 2
    assert state.plan.status == TaskStatus.IN_PROGRESS
    assert mock_chain_invoke.called


@pytest.mark.unit
def test_researcher_agent(mock_chain_invoke, mock_tools) -> None:
    state = NexusState(user_query="Test")
    state.plan.tasks.append(ResearchTask(description="Task 1", status=TaskStatus.PENDING))
    agent = ResearcherAgent()
    
    mock_chain_invoke.side_effect = [
        SearchQueryOutput(query="Test query"),
        FindingsOutput(
            findings=[
                Evidence(task_id="t1", content="Mock evidence content", source="mock.com")
            ]
        )
    ]
    
    output = agent.execute(state)
    
    # Should resolve the single task and move to FactChecker
    assert output.status == "success"
    assert state.plan.tasks[0].status == TaskStatus.COMPLETED
    assert len(state.evidence) == 1
    assert state.current_agent == AgentName.FACT_CHECKER
    assert mock_chain_invoke.call_count == 2


@pytest.mark.unit
def test_fact_checker_success(mock_chain_invoke) -> None:
    state = NexusState(user_query="Test")
    e = Evidence(task_id="t1", content="test", source="mock-source.com")
    state.evidence.append(e)
    agent = FactCheckerAgent()
    
    mock_chain_invoke.return_value = FactCheckerOutput(
        evaluations=[
            ValidationResult(id=e.id, validated=True, validation_reason="Looks good.")
        ]
    )
    
    output = agent.execute(state)
    
    assert output.status == "success"
    assert state.current_agent == AgentName.ANALYST
    assert state.evidence[0].validated is True


@pytest.mark.unit
def test_fact_checker_rejection(mock_chain_invoke) -> None:
    state = NexusState(user_query="Test")
    e = Evidence(task_id="t1", content="test", source="bad-source.com")
    state.evidence.append(e)
    agent = FactCheckerAgent()
    
    mock_chain_invoke.return_value = FactCheckerOutput(
        evaluations=[
            ValidationResult(id=e.id, validated=False, validation_reason="Fake news.")
        ]
    )
    
    output = agent.execute(state)
    
    assert output.status == "success"
    assert state.current_agent == AgentName.RESEARCHER  # Loop back
    assert state.evidence[0].validated is False
    assert len(state.errors) == 1
