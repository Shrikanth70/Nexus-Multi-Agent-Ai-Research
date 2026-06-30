# 🧪 Testing AI Systems
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 3 - Development Standards

Testing non-deterministic systems (LLMs) requires a different approach than traditional software. We use a multi-tiered testing strategy.

---

## 1. Unit Testing (Deterministic)

Agents and tools consist of a lot of deterministic code wrapped around an LLM call. We test the wrapper heavily.
* **Mocking:** We mock the LLM API response to ensure our state parsing, error handling, and tool execution logic works perfectly.
* **State Transitions:** Test the Orchestrator with mock state objects to ensure routing works (e.g., if errors > 0, it routes back to Researcher).

## 2. Integration Testing (The Sandbox)

Test the system connecting to a *local* or very cheap LLM.
* Ensures API keys load, network calls succeed, and basic prompt formatting doesn't crash the system.

## 3. Evaluation (LLM-as-a-Judge)

Because output text varies, we cannot assert `output == "Hello World"`. We use Evaluation frameworks.
* We run the agent against a test dataset of 50 queries.
* A separate, stronger LLM (e.g., GPT-4) acts as a Judge, grading the agent's output on:
  * Factuality (Does it align with the source text?)
  * Formatting (Is it strict JSON?)
  * Relevance (Did it answer the prompt?)

*No new agent prompt is merged to main unless it passes the Evaluation suite.*
