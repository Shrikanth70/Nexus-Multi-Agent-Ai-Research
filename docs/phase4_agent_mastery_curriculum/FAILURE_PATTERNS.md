# ⚠️ Failure Patterns
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

Agents will fail. Websites will go down, context windows will overflow, and LLMs will hallucinate. An enterprise-grade system is defined by how it handles these failures.

---

## 1. The Infinite Loop

**The Scenario:** 
1. Fact Checker says: "Evidence lacks primary source."
2. Researcher searches the same blog again, returns same evidence.
3. Fact Checker rejects again. (Repeat infinitely).

**The Solution:**
* **Orchestrator Limits:** Hard cap loops at 3.
* **State Checkpoints:** When loop limit is hit, revert the `Shared State` to the version before the loop started and route to a Human-in-the-Loop approval queue.
* **Explicit Context:** Pass the exact rejection reason into the Researcher's next prompt: *"You previously failed because: [Reason]. You MUST try a different search strategy."*

## 2. JSON Parsing Failures

**The Scenario:**
The agent is supposed to output `{"validated": true}`, but it outputs ```json\n{"validated": true}\n``` or `{"validated": True}` (Python style).

**The Solution:**
* Use robust parsers (like Pydantic) that attempt to coerce data types.
* If parsing fails, do NOT crash. Catch the exception, and send an automated message back to the LLM: *"Your output was invalid JSON. Error: [Stack Trace]. Please fix formatting and try again."*

## 3. Context Window Overflow

**The Scenario:**
The user uploads a 1,000-page PDF. The agent tries to stuff it all into the prompt. The API returns a `400 Token Limit Exceeded` error.

**The Solution:**
* Implement hard token counting (using `tiktoken`) *before* making the API call.
* If tokens > limit, gracefully degrade: automatically trigger a summarization agent, or slice the oldest items out of the `evidence` array.
