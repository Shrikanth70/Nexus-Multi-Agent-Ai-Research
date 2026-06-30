"""
LangGraph Orchestration Layer.

Replaces the raw while-loop Orchestrator from Phase 1 with an industry-standard
StateGraph execution engine. This enables advanced features like checkpoints,
human-in-the-loop, and parallel execution.
"""

from typing import Dict, Any, Literal
import structlog
from langgraph.graph import StateGraph, START, END

from nexus.core.state import AgentName, NexusState
from nexus.core.exceptions import MaxRetriesExceededError
from nexus.config import settings

from nexus.agents.planner import PlannerAgent
from nexus.agents.researcher import ResearcherAgent
from nexus.agents.fact_checker import FactCheckerAgent
from nexus.agents.analyst import AnalystAgent
from nexus.agents.writer import WriterAgent
from nexus.agents.reviewer import ReviewerAgent

logger = structlog.get_logger(__name__)

# Initialize agents
agents = {
    AgentName.PLANNER: PlannerAgent(),
    AgentName.RESEARCHER: ResearcherAgent(),
    AgentName.FACT_CHECKER: FactCheckerAgent(),
    AgentName.ANALYST: AnalystAgent(),
    AgentName.WRITER: WriterAgent(),
    AgentName.REVIEWER: ReviewerAgent(),
}

def create_agent_node(agent_name: AgentName):
    """Factory to create a LangGraph node function for an agent."""
    agent = agents[agent_name]
    
    def node_func(state: NexusState) -> NexusState:
        # Loop limit protection
        if state.retry_count >= settings.nexus_max_retry_count:
            logger.error("Max retries exceeded", session_id=state.session_id)
            state.is_paused_for_human = True
            state.current_agent = AgentName.SYSTEM
            # Returning the state here instead of raising allows LangGraph to persist the error state.
            return state
            
        logger.info(f"Node execution: {agent_name.value}")
        return agent.execute(state)
        
    return node_func

def router(state: NexusState) -> str:
    """
    Deterministic router based on the mutated current_agent field.
    """
    if state.is_paused_for_human or state.current_agent == AgentName.SYSTEM:
        return END
        
    return state.current_agent.value

def compile_workflow():
    """
    Builds and compiles the LangGraph StateGraph.
    """
    # 1. Define the State
    workflow = StateGraph(NexusState)
    
    # 2. Add Nodes
    for name in AgentName:
        if name != AgentName.SYSTEM:
            workflow.add_node(name.value, create_agent_node(name))
            
    # 3. Add Edges
    # Entry point
    workflow.add_edge(START, AgentName.PLANNER.value)
    
    # Routing edges
    # Each node outputs a state. The router looks at state.current_agent to pick the next node.
    for name in AgentName:
        if name != AgentName.SYSTEM:
            # We map the possible outputs of the router to the node names
            workflow.add_conditional_edges(
                name.value,
                router,
                {n.value: n.value for n in AgentName if n != AgentName.SYSTEM} | {END: END}
            )
            
    # 4. Compile
    return workflow.compile()

# Global compiled graph
app = compile_workflow()
