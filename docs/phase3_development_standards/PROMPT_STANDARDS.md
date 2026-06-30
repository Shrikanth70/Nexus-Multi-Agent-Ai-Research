# 📝 Prompt Standards
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 3 - Development Standards

In Nexus, prompts are treated as critical infrastructure code. They must be version-controlled, highly structured, and designed to enforce strict agent boundaries.

---

## 1. System Prompt Structure

Every agent's system prompt should follow a standard template:

### A. Persona & Role
Define exactly who the agent is and what its single responsibility is.
> "You are the Nexus Fact Checker. Your sole responsibility is to evaluate evidence gathered by Researchers against the user's constraints."

### B. Input Context
Define what the agent is looking at.
> "You will receive an array of `Evidence` objects and the original `UserQuery`."

### C. Execution Rules
Strict boundaries to prevent hallucination or scope creep.
> "- DO NOT conduct new research.
> - DO NOT write the final report.
> - If the evidence is insufficient, you MUST return `validated: false` and provide a `reason`."

### D. Output Format Definition
Agents must output structured data.
> "You must respond in strict JSON format matching the following schema: { ... }"

## 2. Managing Context Windows

* **Dynamic Injection:** Never hardcode facts into prompts. Inject context dynamically from the `Shared State`.
* **Token Economy:** Strip out HTML tags, excessive whitespace, and irrelevant conversational history before injecting it into the prompt.

## 3. Prompt Versioning

Because a small tweak to a prompt can drastically alter an agent's behavior, prompts should ideally be tracked in source control, potentially alongside evaluation metrics proving that Version 2 is better than Version 1.
