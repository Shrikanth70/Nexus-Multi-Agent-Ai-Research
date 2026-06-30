# 🔭 Observability
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

Observability in Multi-Agent systems is not just about server uptime; it is about **cognitive traceability**. If an agent makes a decision, we must know exactly *why*.

---

## The "No Black Boxes" Rule

In traditional software, we log errors and API calls. In Nexus, we must log **Agent Reasoning**.

### 1. Tracing the Graph
Every time the orchestrator moves from one node to another, a trace is emitted.
* `[TIME] [SESSION_ID] Transition: Planner -> Researcher`

### 2. Tracing the Prompts and Completions
Every interaction with the LLM is recorded. We must store the exact prompt sent and the exact JSON returned. This is essential for debugging hallucination.

### 3. Tracing Tool Executions
When an agent uses a tool, we log:
* The Tool Name
* The Arguments provided by the agent.
* The exact string/data returned by the tool.
* Latency and success state.

---

## Implementation Strategies

### Telemetry Systems
Nexus will utilize standard telemetry frameworks (e.g., OpenTelemetry) to structure these logs.
* **Spans:** A full user research request is the Root Span.
* **Child Spans:** The Planner's execution is a child span. A tool call by the Planner is a child of that span.

### The Observable UI
Because we structure state and emit WebSocket events (see `API.md`), the Frontend UI acts as the ultimate observability dashboard. Users don't just see a loading spinner; they see a live feed of:
* *"Planner is breaking down your task..."*
* *"Researcher is searching Google for 'Agentic AI'..."*
* *"Fact Checker rejected evidence due to outdated source..."*

### Cost Observability
Every LLM call returns token usage (prompt tokens, completion tokens). Nexus intercepts this data and attaches a monetary cost estimate to the trace. This prevents bill shock and identifies inefficient agent prompts.
