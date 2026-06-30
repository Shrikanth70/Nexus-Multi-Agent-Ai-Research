"""Tests for the LangGraph Orchestration Layer."""

import pytest

from nexus.core.state import AgentName, NexusState
from nexus.core.graph import router


@pytest.mark.unit
def test_router_normal_flow() -> None:
    """Test that the router correctly routes to the current_agent."""
    state = NexusState(user_query="Test")
    state.current_agent = AgentName.RESEARCHER
    
    next_node = router(state)
    assert next_node == AgentName.RESEARCHER.value


@pytest.mark.unit
def test_router_end_flow() -> None:
    """Test that the router routes to END if the workflow is complete."""
    from langgraph.graph import END
    
    state = NexusState(user_query="Test")
    state.current_agent = AgentName.SYSTEM
    
    next_node = router(state)
    assert next_node == END


@pytest.mark.unit
def test_router_human_pause() -> None:
    """Test that the router stops execution if paused for human."""
    from langgraph.graph import END
    
    state = NexusState(user_query="Test")
    state.current_agent = AgentName.RESEARCHER
    state.is_paused_for_human = True
    
    next_node = router(state)
    assert next_node == END
