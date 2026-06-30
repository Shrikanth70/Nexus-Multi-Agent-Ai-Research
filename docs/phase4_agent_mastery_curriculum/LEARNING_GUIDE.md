# 📚 Learning Guide
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

Welcome to the Nexus Curriculum. This repository is designed to be read alongside the execution of the code. Do not just read these guides; trace the code that implements them.

---

## How to use this Curriculum

We recommend studying the concepts in the following order:

1. **[Agent Engineering](AGENT_ENGINEERING.md):** Learn how we bound LLMs into specialized roles using strict system prompts and structured output requirements.
2. **[Orchestration](ORCHESTRATION.md):** Learn how we string multiple agents together using Directed Acyclic Graphs (DAGs) and State Machines.
3. **[Memory Systems](MEMORY_SYSTEMS.md):** Understand the difference between Working Memory (State) and Episodic Memory (Logs).
4. **[Context Engineering](CONTEXT_ENGINEERING.md):** Master the art of feeding the LLM exactly what it needs, and nothing more.
5. **[Tool Calling](TOOL_CALLING.md):** See how agents interact with the outside world via sandboxed Python functions.
6. **[RAG Guide](RAG_GUIDE.md):** Deep dive into Vector databases and semantic search for the Researcher agent.
7. **[Failure Patterns](FAILURE_PATTERNS.md):** Learn about infinite loops, JSON parsing errors, and hallucination loops.
8. **[Evaluation](EVALUATION.md):** Learn how to quantitatively prove your agent workflow actually works using "LLM-as-a-judge".
9. **[Scaling Guide](SCALING_GUIDE.md):** How to take this architecture and deploy it securely to a production enterprise environment.

## The "Trace the Code" Challenge
For every guide you read above, find the corresponding Python or TypeScript file in the repository and add an inline comment explaining *how* that code implements the concept.
