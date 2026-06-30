# 🗃️ Memory Systems
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

This guide dives deeper into the practical implementation of the memory tiers defined in `MEMORY.md`.

---

## 1. Managing Working Memory (The State)

The `Shared State` grows as the workflow progresses. If a research task requires 50 web searches, the `evidence` array will become massive, eventually exceeding the LLM's context window.

**Techniques for State Management:**
* **Summarization:** Before passing the state to the Writer, a "Summarizer" agent can condense the `evidence` array into key bullet points.
* **Pagination:** Only pass the most recent 5 pieces of evidence in the prompt, while keeping the rest in the database.

## 2. Implementing Episodic Memory

When a user asks: *"Why did you write this paragraph?"*, the system must query its Episodic Memory.

**Implementation:**
* Every time the `Shared State` mutates, we calculate the diff.
* We write the diff to the `State_Checkpoints` PostgreSQL table.
* To answer the user's question, a special "Retrospective Agent" pulls the checkpoint logs for the Writer agent and explains the reasoning step based on the exact state that existed at that exact millisecond.

## 3. The Illusion of Memory in Chatbots

Standard chatbots pass the entire chat history back and forth to simulate memory.
* `User: Hi`
* `Bot: Hello`
* `User: My name is Alice`
* `Bot: Nice to meet you Alice`

In Nexus, we convert conversational history into **Semantic State**.
Instead of passing the raw chat logs, an agent updates the state:
`state.user_profile.name = "Alice"`.
This is infinitely more robust and scalable than relying on the LLM to continually re-read raw chat transcripts.
