# 🧠 Memory Systems
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

In multi-agent systems, agents need to recall past events, facts, and context to avoid repeating work or hallucinating. We implement four distinct tiers of memory.

---

## 1. Working Memory (The Shared State)

**Purpose:** Short-term context for the current execution cycle.
**Implementation:** The strictly typed JSON object passed between agents (see `STATE.md`).
**Scope:** Exists only for the duration of a single user request or active workflow.
**Usage:**
* Storing the current task list.
* Holding recently gathered evidence.
* Storing draft paragraphs.

## 2. Episodic Memory (The Audit Log)

**Purpose:** Remembering *what happened* in the past.
**Implementation:** A database table logging every state transition, tool call, and agent action with timestamps.
**Scope:** Persistent per-session or per-user.
**Usage:**
* "What did the Researcher agent do 5 minutes ago?"
* "Why did the Fact Checker reject this claim?"
* Resuming a workflow after a human-in-the-loop pause.

## 3. Semantic Memory (The Knowledge Base)

**Purpose:** Remembering *facts* and validated information across sessions.
**Implementation:** A Knowledge Graph or structured SQL database of verified entities and relationships.
**Scope:** Global across the entire platform.
**Usage:**
* "What is the official definition of Agentic AI we agreed on last week?"
* Preventing the system from researching the exact same topic twice.

## 4. Vector Memory (RAG / The Library)

**Purpose:** Recalling large volumes of unstructured text and documents.
**Implementation:** A Vector Database (e.g., pgvector, Pinecone) storing document embeddings.
**Scope:** Global or scoped per-project.
**Usage:**
* The Researcher agent queries the Vector Database to find relevant paragraphs from a 500-page PDF uploaded by the user.

---

## The Challenge of Context Windows

LLMs have limited context windows. If we stuff all historical memory into every prompt, the model gets confused and costs skyrocket. 

**The Solution:**
Agents must actively *query* memory as a Tool, rather than having it injected implicitly. For example, the Researcher agent might have a tool: `search_vector_database(query="agentic workflows")`. This ensures memory retrieval is an explicit, observable action.
