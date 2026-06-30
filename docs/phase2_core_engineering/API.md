# 🌐 API Design
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

The Nexus API must support standard CRUD operations, but more importantly, it must handle **long-running, asynchronous AI workflows** and **stream real-time updates** to the UI.

---

## Core API Paradigms

### 1. RESTful Endpoints (Standard CRUD)
Used for managing users, workspaces, and retrieving historical sessions.
* `GET /api/v1/sessions`
* `GET /api/v1/sessions/{id}`

### 2. Asynchronous Execution (The Orchestrator)
When a user submits a complex research query, the system might take 5 minutes to plan, research, and write. We cannot hold an HTTP connection open that long.
* `POST /api/v1/research/start`
  * **Input:** `{ "query": "..." }`
  * **Response:** `{ "session_id": "req_123", "status": "processing" }` (Returns immediately)

### 3. WebSockets / Server-Sent Events (SSE)
To achieve the "Observable UI," the UI must know exactly what the agents are doing in real-time.
* `WS /api/v1/sessions/{id}/stream`
* **Payloads pushed to UI:**
  * `{ "event": "agent_started", "agent": "Planner" }`
  * `{ "event": "tool_call", "tool": "web_search", "query": "Agentic AI" }`
  * `{ "event": "state_update", "diff": { ... } }`

---

## Human-in-the-Loop (HITL) Endpoints

The system must allow humans to intervene, approve, or correct the AI workflow.

### The Pause
When the orchestrator hits a breakpoint (e.g., Fact Checker finished), it changes the session status to `awaiting_approval`.

### The Intervention Endpoints
* `POST /api/v1/sessions/{id}/approve`
  * Resumes the graph execution.
* `POST /api/v1/sessions/{id}/override`
  * **Payload:** Explicit mutations to the `Shared State`.
  * **Use Case:** A human corrects a bad piece of evidence before allowing the Writer agent to proceed.

---

## API Security

* All endpoints require JWT authentication.
* API rate limiting is critical to prevent runaway LLM costs.
* Tool execution endpoints must be strictly internal and never exposed directly to the public API without sanitization.
