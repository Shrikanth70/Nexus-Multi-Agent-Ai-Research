# 🔄 Workflows & Orchestration
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

Nexus models its agent interactions as a **directed graph** or a **state machine**. The orchestrator evaluates the Shared State and determines which agent should activate next.

---

## Workflow Topologies

### 1. Sequential (Chain)
The simplest topology.
`Planner -> Researcher -> Writer`
* **Use Case:** Simple, highly predictable tasks where each step strictly depends on the previous one.

### 2. Parallel (Fan-out / Fan-in)
`Planner -> [Researcher A, Researcher B, Researcher C] -> Writer`
* **Use Case:** The Planner breaks a complex query into 3 distinct sub-topics. Three Researcher agents are spun up in parallel to gather evidence faster. The orchestrator waits for all to finish before routing to the Writer.

### 3. Conditional Routing (Loops)
`Researcher -> Fact Checker -> (If Fail) -> Researcher`
* **Use Case:** Quality control. The Fact Checker evaluates the evidence. If the evidence is insufficient, it modifies the state with an error and routes control *back* to the Researcher to try again.

---

## The Orchestrator Implementation

The orchestrator is not an LLM. It is standard, deterministic software logic.

```python
def orchestrate(state: NexusState):
    if state.current_agent == "Planner":
        new_state = run_planner(state)
        # Transition logic
        new_state.current_agent = "Researcher"
        return new_state
        
    if state.current_agent == "Researcher":
        new_state = run_researcher(state)
        new_state.current_agent = "FactChecker"
        return new_state
        
    if state.current_agent == "FactChecker":
        new_state = run_fact_checker(state)
        if new_state.errors:
            new_state.current_agent = "Researcher" # Loop back
        else:
            new_state.current_agent = "Writer"
        return new_state
```

## Guarding Against Infinite Loops

A major risk in autonomous AI workflows is the infinite loop (e.g., Fact Checker continually rejecting Researcher, Researcher continually returning the same bad data).

**Mitigation:**
1. **Loop Counters:** The State object must include a `retry_count`. If `retry_count > 3`, the orchestrator routes to a Human-in-the-Loop or a graceful failure state.
2. **Explicit Feedback:** When rejecting, the Fact Checker must provide explicit `RejectionReasons` in the state so the Researcher knows exactly *why* it failed and what to do differently.
