# 🗄️ Database Architecture
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

The persistence layer of Nexus must handle three entirely different types of data: highly structured relational data (sessions, users), semi-structured JSON data (state checkpoints), and unstructured high-dimensional vectors (embeddings).

To minimize infrastructure complexity while maintaining enterprise-grade capabilities, we standardize on **PostgreSQL**, leveraging specific extensions.

---

## Primary Datastore: PostgreSQL

### 1. Relational Tables (The Scaffolding)
Standard relational tables for application management.
* `Users`: Authentication and profiles.
* `Workspaces`: Tenant isolation for enterprise deployments.
* `Sessions`: High-level tracking of a research request.

### 2. JSONB Columns (State Checkpoints)
Because the `Shared State` is a strictly typed JSON object that mutates over time, we store it in a `JSONB` column.
* `State_Checkpoints`: 
  * `session_id` (UUID)
  * `step_number` (Integer)
  * `agent_name` (String)
  * `state_payload` (JSONB)
* *Why:* This allows us to query deep within the JSON structure (e.g., "Find all sessions where the Fact Checker rejected evidence") while easily enabling "time travel" by pulling a specific `step_number`'s state.

### 3. Vector Columns (pgvector)
For RAG (Retrieval Augmented Generation) and Long-term memory.
* `Document_Chunks`:
  * `id` (UUID)
  * `content` (Text)
  * `embedding` (Vector)
  * `metadata` (JSONB - for pre-filtering)
* *Why `pgvector`:* Keeps data unified. No need to manage a separate vector database (like Pinecone) unless scaling requires it.

---

## Data Privacy and Tenancy

In an enterprise environment, research data is highly sensitive.
* **Row-Level Security (RLS):** PostgreSQL RLS will be enforced to ensure no workspace can query vectors or state checkpoints belonging to another workspace.
* **Ephemeral Mode:** Support for requests where the `State_Checkpoints` are kept strictly in Redis/Memory and purged immediately upon completion, bypassing persistent storage entirely.
