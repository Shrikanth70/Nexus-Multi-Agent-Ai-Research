# 🤝 Contributing to Nexus
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 3 - Development Standards

Welcome to the Nexus Research Intelligence Platform. We are building the premier educational codebase for learning Agentic AI through production engineering.

---

## The Golden Rule of Contributions

Before submitting a PR, you must be able to answer this question:
> **"What important Multi-Agent or AI Engineering concept does this teach?"**

If your PR simply adds a new API wrapper without illustrating a core architectural principle, it may be rejected to keep the codebase focused on learning.

## How to Contribute

1. **Check the ADRs:** Read the Architecture Decision Records (`docs/ADRs`) to understand *why* the system is built the way it is.
2. **Open an Issue:** Discuss your idea before writing code. Propose how it fits into the `PROJECT_VISION.md`.
3. **Write Tests:** If you are adding an agent, add an evaluation test. If you are adding a tool, add a unit test.
4. **Update the Curriculum:** If your feature introduces a new concept (e.g., a new RAG technique), you must update the relevant document in Phase 4 (e.g., `RAG_GUIDE.md`).

## PR Review Process

Reviews will focus heavily on:
* **Observability:** Did you add telemetry spans?
* **State Management:** Are you modifying state correctly without side effects?
* **Code Clarity:** Is the logic framework-agnostic and clean?
