# 📦 State
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 1 - Foundation

State is the most important concept in a reliable Multi-Agent System. If agents communicate via hidden text prompts and chat history, the system becomes fragile, unpredictable, and unobservable.

In Nexus, **all communication and context is passed through a strictly typed Shared State Object.**

---

## The Philosophy of Explicit State

1. **No Hidden Conversations:** Agents do not DM each other. If the Researcher has findings for the Writer, it places them in the `state.evidence` array.
2. **Typed Data:** State is not a string. It is a strictly typed object (e.g., JSON Schema, Pydantic, Zod).
3. **Immutability and History:** We append to state or track state transitions so we can "time travel" to any point in the workflow for debugging.

---

## Example State Schema

Below is a conceptual representation of the `NexusState` object that travels through the graph.

```json
{
  "session_id": "req_12345abc",
  "user_query": "Analyze the impact of Agentic AI on Enterprise software architecture.",
  
  "plan": {
    "status": "completed",
    "tasks": [
      { "id": "t1", "description": "Define Agentic AI", "status": "completed" },
      { "id": "t2", "description": "Identify impacts on Enterprise Architecture", "status": "pending" }
    ]
  },

  "evidence": [
    {
      "task_id": "t1",
      "content": "Agentic AI refers to systems capable of autonomous planning and tool execution...",
      "source": "https://example.com/ai-paper",
      "validated": true
    }
  ],

  "draft": {
    "content": null,
    "revisions": 0
  },

  "errors": [],
  "current_agent": "Researcher"
}
```

---

## How Agents Interact with State

* **The Planner** reads `user_query` and populates the `plan.tasks` array.
* **The Researcher** reads `plan.tasks`, executes pending ones, and populates the `evidence` array.
* **The Fact Checker** reads `evidence`, changes `validated: true|false`, and populates `errors` if needed.
* **The Writer** reads `validated` evidence and populates `draft.content`.

## Benefits of Typed State
* **Resilience to Hallucination:** Since the Writer agent only receives the `evidence` array (and is explicitly told to *only* use that array), it cannot hallucinate facts from its base weights as easily.
* **Observability:** We can render the UI directly from this JSON object. A user can watch the `evidence` array grow in real-time.
* **Human-in-the-Loop:** A human can easily pause the workflow, manually edit an object in the `evidence` array, and resume the graph.
