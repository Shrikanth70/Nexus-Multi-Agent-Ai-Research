# 🔀 Orchestration
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

If Agents are the musicians, the Orchestrator is the conductor. It dictates who plays, when they play, and when they stop.

---

## State Machines as Orchestrators

Nexus does not use LLMs to decide who should speak next (that is highly unpredictable). It uses deterministic code based on the `Shared State`.

### Example Workflow: The Feedback Loop

1. **State:** `current_agent: "Researcher"`, `errors: []`
2. **Action:** Orchestrator calls `Researcher` function.
3. **Action:** `Researcher` adds evidence to state, updates `current_agent: "FactChecker"`.
4. **Action:** Orchestrator calls `FactChecker`.
5. **Action:** `FactChecker` finds a flaw. It adds to `errors` array, and updates `current_agent: "Researcher"`.
6. **Action:** Orchestrator calls `Researcher` again, but this time the Researcher sees the `errors` array and knows it must fix its previous mistake.

## Parallel Execution

When the Planner breaks a query into three distinct sub-tasks:
* The Orchestrator can spin up three parallel threads/async tasks.
* Each thread passes a *copy* of the state to a Researcher agent.
* **The Fan-in Problem:** When the three Researchers finish, the Orchestrator must safely merge their evidence arrays back into the single `Shared State` without race conditions.

## The Router Pattern

Sometimes we *do* use an LLM for orchestration. This is called a **Router Agent**.
* **Use Case:** A user uploads a file. Is it a dataset (needs Code Interpreter) or a policy document (needs RAG)?
* **Implementation:** A tiny, fast LLM call whose sole job is to classify the request and update `state.next_workflow = "data_analysis" | "document_qa"`.
