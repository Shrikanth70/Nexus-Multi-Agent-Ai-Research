<h1 align="center">
  🧠 Nexus Research Intelligence Platform
</h1>

<p align="center">
  <strong>Enterprise-Grade Multi-Agent AI Research System</strong><br/>
  An educational, production-inspired open-source reference implementation for learning Agentic AI.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white"/>
  <img src="https://img.shields.io/badge/Phase-1%20Foundation-6366f1?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square"/>
  <img src="https://img.shields.io/badge/Theme-Bright%20Only-f59e0b?style=flat-square"/>
</p>

---

## What Is Nexus?

Nexus is **not a chatbot**.

It is a complete simulation of an AI-powered research organization, built to teach Multi-Agent Systems through production-grade software engineering.

Instead of one LLM answering a question, Nexus deploys a **team of specialized agents**:

```
User Query
    ↓
Planner Agent      — breaks the problem into tasks
    ↓
Researcher Agent   — gathers raw evidence from the web
    ↓
Fact Checker Agent — validates every claim for credibility
    ↓
Analyst Agent      — synthesizes patterns and insights
    ↓
Writer Agent       — composes the structured report
    ↓
Reviewer Agent     — ensures quality and alignment with the original query
    ↓
Final Report
```

Every architectural decision is intentional and teaches an important concept in Multi-Agent Systems.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend Client (UI)                          │
│              Bright Theme — Notion/Linear/Perplexity style           │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTPS / WebSocket
┌───────────────────────────▼─────────────────────────────────────────┐
│                      API Gateway (FastAPI)                            │
│         REST + SSE/WebSocket + HITL Intervention Endpoints           │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                   Orchestration Layer (State Machine)                 │
│         Deterministic routing based on NexusState evaluation         │
│   ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌────────────────┐   │
│   │ Workflow  │  │ Planning │  │  Routing & │  │ Human-in-Loop  │   │
│   │  Engine  │  │& Decomp. │  │ Scheduling │  │  (Approvals)   │   │
│   └──────────┘  └──────────┘  └────────────┘  └────────────────┘   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │  Reads/Mutates NexusState
┌───────────────────────────▼─────────────────────────────────────────┐
│                      Agent Layer (6 Specialists)                      │
│  ┌─────────┐ ┌──────────┐ ┌───────────┐ ┌─────────┐ ┌──────────┐  │
│  │ Planner │ │Researcher│ │FactChecker│ │ Analyst │ │  Writer  │  │
│  └─────────┘ └──────────┘ └───────────┘ └─────────┘ └──────────┘  │
│                                              ┌──────────┐            │
│                                              │ Reviewer │            │
│                                              └──────────┘            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                 Shared State & Communication Bus                      │
│        NexusState (typed JSON) — the single source of truth          │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│  Data Layer   │ │ Observability  │ │  Tools Layer   │
│ PostgreSQL     │ │  structlog     │ │ Web Search     │
│ ChromaDB       │ │  OpenTelemetry │ │ Doc Loader     │
│ Redis          │ │  Traces/Spans  │ │ Code Interp.   │
└────────────────┘ └────────────────┘ └────────────────┘
```

---

## Learning Outcomes

By studying and extending this codebase, you will understand:

| Concept | Where It Lives |
|---|---|
| Agent abstraction + Single Responsibility | `nexus/agents/base.py` |
| Typed Shared State (Working Memory) | `nexus/core/state.py` |
| Deterministic Orchestration (State Machine) | `nexus/core/orchestrator.py` |
| Prompt Engineering + Agent Drift Prevention | `nexus/prompts/` |
| Structured Observability (No Black Boxes) | `nexus/observability/logger.py` |
| Tool Calling + Sandboxed Execution | `nexus/tools/` _(Phase 3)_ |
| RAG + Vector Memory | `nexus/memory/` _(Phase 3)_ |
| REST + WebSocket API | `nexus/api/` _(Phase 4)_ |
| Human-in-the-Loop | `nexus/api/hitl.py` _(Phase 4)_ |
| LLM-as-Judge Evaluation | `nexus/evaluation/` _(Phase 4)_ |

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | Python 3.11+ | Type hints, async/await, ecosystem |
| State Schemas | Pydantic v2 | Runtime validation at LLM boundaries |
| Orchestration | Raw Python → LangGraph (Phase 2) | Learn fundamentals before frameworks |
| LLM Runtime | Ollama (local) + OpenAI/Anthropic adapters | Free, open-source first |
| Vector DB | ChromaDB (Phase 3) → pgvector (Phase 4) | Local learning → production scale |
| Persistence | PostgreSQL + Redis | Relational + cache/queue |
| API | FastAPI + WebSockets | Async AI-native API design |
| Observability | structlog + OpenTelemetry + Langfuse | Full cognitive traceability |
| Frontend (temp) | Streamlit | Rapid state visualization |
| Frontend (final) | Next.js / React | Phase 5 production UI |
| Linting | Ruff | Fast, modern Python linting |
| Type Checking | mypy (strict) | Enterprise-grade type safety |
| Testing | pytest + pytest-cov | Unit, integration, evaluation |

---

## Project Structure

```
nexus/
├── pyproject.toml                 # Project deps, Ruff, mypy, pytest config
├── .env.example                   # Environment variable template (safe to commit)
├── .gitignore
├── README.md
│
├── nexus/                         # Core Python package
│   ├── core/
│   │   ├── state.py               # NexusState — the Shared State schema (Pydantic)
│   │   ├── orchestrator.py        # Deterministic state machine orchestrator
│   │   └── exceptions.py          # Custom exception hierarchy
│   │
│   ├── agents/
│   │   ├── base.py                # BaseAgent abstract class
│   │   ├── planner.py             # Planner Agent (task decomposition)
│   │   ├── researcher.py          # Researcher Agent (evidence gathering)
│   │   ├── fact_checker.py        # Fact Checker Agent (validation)
│   │   ├── analyst.py             # Analyst Agent (synthesis/patterns)
│   │   ├── writer.py              # Writer Agent (report drafting)
│   │   └── reviewer.py            # Reviewer Agent (quality control)
│   │
│   ├── prompts/                   # System prompts (version-controlled infrastructure)
│   │
│   ├── observability/
│   │   └── logger.py              # structlog config + trace emitters
│   │
│   └── config.py                  # Pydantic Settings (env var loading)
│
├── tests/
│   ├── unit/
│   │   ├── test_state.py          # State schema validation tests
│   │   ├── test_orchestrator.py   # Routing + loop limit tests
│   │   └── test_agents.py         # Mock agent output tests
│   └── conftest.py
│
├── docs/
│   ├── phase1_foundation/         # Architecture + Vision docs
│   ├── phase2_core_engineering/   # Memory, Tools, API docs
│   ├── phase3_development_standards/
│   │   └── ADRs/                  # Architecture Decision Records
│   └── phase4_agent_mastery_curriculum/
│
└── frontend.py                    # Streamlit UI (Phase 1 visualization)
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [Ollama](https://ollama.com/) (for local LLM — free, no API key required)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/nexus.git
cd nexus

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Configure environment
cp .env.example .env
# Edit .env — set LLM_PROVIDER=ollama for local development

# 5. (Optional) Pull a local LLM via Ollama
ollama pull llama3
```

### Run the Streamlit UI

```bash
streamlit run frontend.py
```

### Run Tests

```bash
pytest tests/ -v -m unit
```

### Code Quality

```bash
# Lint + format
ruff check nexus/ tests/
ruff format nexus/ tests/

# Type checking
mypy nexus/
```

---

## Implementation Roadmap

| Phase | Focus | Status |
|---|---|---|
| **Phase 1** | Foundation: State schemas, Mock agents, Orchestrator, Observability | 🟡 In Progress |
| **Phase 2** | Core Engineering: Real LLMs, LangGraph, Full agent workflow | ⏳ Planned |
| **Phase 3** | Systems & Tools: Web search, ChromaDB/RAG, Episodic memory | ⏳ Planned |
| **Phase 4** | Enterprise Grade: FastAPI, WebSockets, HITL, Evaluation | ⏳ Planned |
| **Phase 5** | UI & Polish: Next.js frontend, Real-time agent graph visualization | ⏳ Planned |

---

## Educational Philosophy

> *"Every feature added to the system must answer one question: What important Multi-Agent concept does this teach?"*

This repository is designed to be read alongside the code. For every module you open, trace it back to the architectural decision that created it. See `docs/phase4_agent_mastery_curriculum/LEARNING_GUIDE.md`.

---

## Contributing

See [CONTRIBUTING.md](docs/phase3_development_standards/CONTRIBUTING.md). All contributions must teach a Multi-Agent Systems concept.

---

## License

MIT License — See [LICENSE](LICENSE) for details.
