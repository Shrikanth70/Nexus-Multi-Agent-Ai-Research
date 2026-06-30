# 🔧 Tool Calling
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

Tool calling (or Function Calling) is the bridge between LLM text generation and deterministic code execution.

---

## 1. How Tool Calling Actually Works

1. **Schema Definition:** We define a Python function (e.g., `get_weather(location: str)`). We convert its signature into a JSON Schema.
2. **System Prompt Injection:** We send the JSON Schema to the LLM and say, "You have access to these tools. If you need to use one, output a JSON object matching this schema."
3. **The Interception:** The LLM outputs `{"name": "get_weather", "arguments": {"location": "London"}}`. 
4. **Execution:** Nexus intercepts this, parses the JSON, and runs the actual Python function `get_weather("London")`.
5. **The Return:** Nexus takes the result (`"15°C, Raining"`), formats it as a "ToolMessage", and sends it *back* to the LLM.

## 2. Best Practices for Agent Tools

### Name and Description are Critical
The LLM decides which tool to use based *entirely* on the name and docstring description.
* **Bad:** `def tool1(q):`
* **Good:** `def search_academic_papers(query: str): """Searches arxiv.org for academic papers matching the query string."""`

### Error Handling
If a tool throws a Python Exception, the agent workflow crashes.
* **Rule:** Tools must catch all exceptions and return them as strings.
* If `requests.get()` times out, the tool should return `"Error: Connection timed out. Try a different URL."` The agent reads this string and knows to try a fallback strategy.

### The "No-Op" Tool
Sometimes an agent thinks it *has* to use a tool. Always provide a way out. In complex graphs, provide a tool like `finish_task()` or `no_action_needed()` so the agent can cleanly yield control back to the Orchestrator.
