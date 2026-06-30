# 🤖 Agent Engineering
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

An agent is more than just an API call to an LLM. It is a software component that encapsulates cognition, memory access, and tool execution bounded by a single responsibility.

---

## 1. The Anatomy of an Agent

In Nexus, an Agent consists of three parts:
1. **The System Prompt:** The persona and the strict rules.
2. **The Output Schema:** The exact Pydantic/Zod schema the LLM must return.
3. **The Wrapper Function:** The Python code that takes the `Shared State`, formats it for the LLM, executes the API call, parses the JSON response, and applies the mutation back to the `Shared State`.

## 2. Preventing "Agent Drift"

**The Problem:** If you tell an LLM "You are a Fact Checker", it might eventually try to rewrite the entire report because LLMs naturally want to be helpful and complete tasks.

**The Solution:**
* **Negative Prompting:** Explicitly list what the agent *cannot* do. (`DO NOT write the draft. DO NOT conduct search.`)
* **Constrained Output:** If the Fact Checker's output schema only allows `{"validated": boolean, "reason": string}`, it *physically cannot* rewrite the report, because the orchestrator will only parse those two fields and discard the rest.

## 3. The Power of Specialized Agents

Why use 5 agents instead of 1 really smart GPT-4 call?
* **Cost:** We can use a cheap, fast model (like Llama 3 8B) for simple extraction tasks, and save the expensive GPT-4 calls for the final Writer synthesis.
* **Accuracy:** By forcing an LLM to only focus on *one* task (e.g., Fact Checking) rather than holding the entire planning, researching, and writing context in its head, hallucination rates drop dramatically.
