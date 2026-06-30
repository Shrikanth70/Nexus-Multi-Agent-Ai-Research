# 💻 Coding Standards
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 3 - Development Standards

To maintain an enterprise-grade codebase, Nexus enforces strict software engineering standards. This is not a hackathon project; it is a reference implementation for production AI.

---

## 1. Core Principles

* **Clean Architecture:** Domain logic (Agent intelligence) must have zero dependencies on infrastructure (Databases, FastApi, UI).
* **Strict Typing:** All data passing between functions, especially LLM boundaries, must be typed (using Pydantic in Python or Zod in TypeScript).
* **Pure Functions Where Possible:** Agents should ideally act as pure functions: `f(state) -> new_state`. This makes them highly testable.

## 2. Language & Formatting

* **Backend:** Python 3.11+
  * *Linter/Formatter:* `Ruff`
  * *Type Checker:* `mypy` (Strict mode)
* **Frontend:** TypeScript / Next.js
  * *Linter/Formatter:* `ESLint` / `Prettier`
* **Commit Messages:** Conventional Commits (`feat:`, `fix:`, `docs:`)

## 3. The "No Magic" Rule

Many AI frameworks hide complexity behind "magic" wrappers. Nexus forbids this.
* If we call an LLM, we use the official provider SDK (e.g., `openai` python package) and handle the request/response explicitly.
* We do not use massive abstraction chains that obscure the exact prompt being sent to the model.

## 4. Documentation

* **Docstrings:** All classes and core functions must have Google-style docstrings.
* **Inline Comments:** Focus on *why*, not *what*. Especially important for prompt construction logic.
