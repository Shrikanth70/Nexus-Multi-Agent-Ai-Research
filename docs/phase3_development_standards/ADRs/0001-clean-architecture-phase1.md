# ADR 0001: Clean Architecture & Raw State Machines for Phase 1

**Date:** 2026-06-30
**Status:** Accepted
**Phase:** 1 - Foundation

## Context
The Nexus Platform aims to be an educational reference implementation for Multi-Agent Systems (MAS). The architecture diagram references **LangGraph** as the orchestration layer. However, introducing a powerful framework like LangGraph immediately obscures the fundamental mechanics of how multi-agent routing actually works (state evaluation and transitions). 

Furthermore, `CODING_STANDARDS.md` explicitly states the "No Magic Rule", requiring domain logic to be framework-agnostic.

## Decision
For Phase 1 (Foundation), we have decided to implement the Orchestrator as a **raw Python deterministic state machine** (`nexus/core/orchestrator.py`) operating on a strictly typed **Pydantic Shared State** (`nexus/core/state.py`), entirely devoid of third-party orchestration frameworks.

We will introduce LangGraph in **Phase 2**, acting as an adapter that wraps our pure Python agent functions.

## Consequences

### Positive Impacts (Why we did this)
1. **Educational Clarity:** Contributors can trace a `while` loop routing between agents, directly observing how `current_agent` mutations dictate control flow.
2. **Framework Agnosticism:** The core `NexusState` and agent logic (`execute(state) -> state`) remain pure. When we swap to LangGraph in Phase 2, the agent domain logic will not need to be rewritten.
3. **Testability:** A raw state machine and pure functions are trivial to unit test without mocking complex framework internals.

### Negative Impacts (Trade-offs)
1. **Refactoring Overhead:** The raw `Orchestrator` class built in Phase 1 will eventually be deprecated and replaced by LangGraph's execution engine in Phase 2.
2. **Parallel Execution Complexity:** Implementing Fan-out/Fan-in (parallel agents) in raw Python is complex; however, since Phase 1 relies on mock agents, we sidestep this concurrency complexity until Phase 2 when LangGraph handles it natively.
