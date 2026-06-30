# 🛠️ Tools
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 2 - Core Engineering

Tools are how agents interact with the outside world. An LLM on its own can only predict text based on past training data; tools give agents the ability to search, read, calculate, and take action.

---

## Tool Design Principles

1. **Sandboxed & Safe:** Tools must not have unbounded access to the system. They operate in a sandbox.
2. **Strictly Typed Inputs:** An agent must provide exact, validated JSON to call a tool (e.g., using OpenAI's Function Calling API).
3. **Graceful Failure:** If a tool fails (e.g., a website returns a 404), the tool must catch the error and return a clear string explanation to the agent (`"Error: The website could not be reached. Try a different URL."`), rather than crashing the system.

---

## Core Tool Library

### 1. Web Search
* **Description:** Searches the public internet.
* **Input:** `query` (string)
* **Output:** List of `urls`, `titles`, and short `snippets`.

### 2. URL Reader / Scraper
* **Description:** Extracts main body text from a specific URL.
* **Input:** `url` (string)
* **Output:** `markdown_text` (string). *Crucial: We must strip HTML and Javascript to save tokens and prevent context window bloat.*

### 3. Vector Database Search (RAG)
* **Description:** Searches internal enterprise documents.
* **Input:** `semantic_query` (string)
* **Output:** Relevant chunks of text from internal PDFs/Docs.

### 4. Calculator / Code Interpreter
* **Description:** Executes Python code to perform math or data analysis securely.
* **Input:** `python_code` (string)
* **Output:** `stdout` or `error_trace`.

---

## The Mechanics of a Tool Call

When an Agent decides to use a tool, the flow is as follows:

1. **LLM Output:** The LLM generates a JSON payload indicating the tool name and arguments.
2. **Validation:** The Nexus framework intercepts this JSON and validates it against the Tool's schema.
3. **Execution:** Nexus executes the underlying Python/TS function.
4. **Observation:** The result of the function is appended to the LLM's context as a "Tool Response".
5. **Synthesis:** The LLM reads the observation and decides what to do next.

*Every tool call must be logged for Observability.*
