"""Tests for the Shared State schemas."""

import pytest
from pydantic import ValidationError

from nexus.core.state import AgentName, Evidence, NexusState, ResearchTask, TaskStatus


@pytest.mark.unit
def test_nexus_state_initialization() -> None:
    """Test that the state initializes correctly with required fields."""
    state = NexusState(user_query="Test query")
    
    assert state.user_query == "Test query"
    assert state.current_agent == AgentName.PLANNER
    assert state.retry_count == 0
    assert not state.is_paused_for_human
    assert len(state.errors) == 0


@pytest.mark.unit
def test_nexus_state_validation_error() -> None:
    """Test that Pydantic enforces required fields."""
    with pytest.raises(ValidationError):
        NexusState()  # type: ignore # Missing user_query


@pytest.mark.unit
def test_add_error_helper() -> None:
    """Test the add_error helper correctly increments retry count."""
    state = NexusState(user_query="Test")
    assert state.retry_count == 0
    
    state.add_error(AgentName.FACT_CHECKER, "Validation failed")
    
    assert state.retry_count == 1
    assert len(state.errors) == 1
    assert state.errors[0].agent_name == AgentName.FACT_CHECKER
    assert state.errors[0].error_message == "Validation failed"


@pytest.mark.unit
def test_evidence_validation() -> None:
    """Test Evidence schema."""
    ev = Evidence(
        task_id="t1",
        content="Fact",
        source="http://test.com"
    )
    assert not ev.validated
    assert ev.validation_reason is None
