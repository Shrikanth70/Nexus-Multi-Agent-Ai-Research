# 🔍 RAG Guide
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

Retrieval-Augmented Generation (RAG) is how we give agents access to private data. It is a specific application of Tool Calling and Vector Memory.

---

## 1. The Basic RAG Pipeline

1. **Ingestion:** A PDF is uploaded -> chunked into 500-word blocks -> embedded using a model (e.g., `text-embedding-3-small`) -> stored in `pgvector`.
2. **Retrieval:** The Researcher agent calls `search_database("agent workflows")`. The query is embedded -> vector similarity search is performed -> top 5 chunks are returned.
3. **Generation:** The chunks are injected into the Researcher's context window.

## 2. Advanced Agentic RAG

Basic RAG fails on complex queries because users don't ask semantic questions; they ask multi-hop questions.

### Pattern: Query Rewriting
Before hitting the database, the Planner agent rewrites the user query.
* *User:* "How does Nexus compare to AutoGPT?"
* *Planner generates 2 queries:* `["Nexus platform architecture", "AutoGPT platform architecture"]`

### Pattern: Document Hierarchies (Parent-Child RAG)
* We embed small chunks (sentences) for highly accurate search matching.
* When a match is found, we retrieve the *Parent* chunk (the whole paragraph) and inject that into the context window, providing the LLM with surrounding context.

### Pattern: Metadata Filtering
Vector search is often fuzzy. We enforce strict metadata filtering.
* If the user asks "Show me research from 2023", the agent must structure its tool call as: `search_database(query="...", year=2023)`. The SQL query filters on the metadata column *before* performing the vector math.
