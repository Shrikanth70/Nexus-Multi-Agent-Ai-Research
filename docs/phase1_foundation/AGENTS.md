# 🕵️ Agents
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 1 - Foundation

In the Nexus Platform, we do not rely on a single omniscient LLM. Instead, we model an **Intelligence Organization** composed of highly specialized experts. Each Agent adheres to the **Single Responsibility Principle**.

---

## The Core Agent Team

### 1. The Planner 🧠
**Responsibility:** Decompose user requests into actionable, sequential tasks.
* **Input:** User query, overall context.
* **Output:** A structured `TaskGraph` or ordered list of `ResearchTasks`.
* **Tools:** None. Pure reasoning and planning.
* **Personality:** Analytical, structured, methodical.

### 2. The Researcher 🔎
**Responsibility:** Execute specific tasks by finding raw data.
* **Input:** A single `ResearchTask`.
* **Output:** A collection of `Evidence` (facts, quotes, data points).
* **Tools:** Web Search, Document Reader, URL Scraper.
* **Personality:** Exhaustive, precise, strictly factual.

### 3. The Fact Checker ⚖️
**Responsibility:** Validate the evidence gathered by the Researcher against constraints.
* **Input:** `Evidence` array.
* **Output:** A boolean approval or a `RejectionReason`.
* **Tools:** Cross-reference tools, logic-check prompts.
* **Personality:** Skeptical, rigorous, uncompromising.

### 4. The Writer ✍️
**Responsibility:** Synthesize validated evidence into a cohesive narrative or report.
* **Input:** Validated `Evidence`, User context.
* **Output:** A `DraftReport`.
* **Tools:** None. Pure synthesis and formatting.
* **Personality:** Articulate, clear, objective.

### 5. The Reviewer 📋
**Responsibility:** Ensure the final draft perfectly aligns with the original user request.
* **Input:** `DraftReport`, User query.
* **Output:** `FinalReport` or a feedback loop back to the Planner/Writer.
* **Tools:** None.
* **Personality:** Critical, user-obsessed, detail-oriented.

---

## Agent Lifecycle and Autonomy

Agents in Nexus are **stateless pure functions** with respect to the orchestrator. They are "woken up," handed the current global state, they perform their specialized duty, mutate the state, and go back to sleep.

They do not "talk" to each other in chat threads. Their collaboration is emergent through the structural modification of the `Shared State`.

### Why this Model Works:
1. **Explainability:** We know exactly *who* failed if bad evidence makes it to the draft (The Fact Checker).
2. **Scalability:** If research is slow, we can spin up 10 parallel Researchers; the Planner and Writer remain unchanged.
3. **Modularity:** We can replace the LLM driving the Planner with an OpenAI model, while using a cheaper, local model for the Fact Checker.
