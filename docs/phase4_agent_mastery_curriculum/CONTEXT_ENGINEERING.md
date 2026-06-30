# 🎯 Context Engineering
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

Context Engineering is the practice of manipulating exactly what information goes into the LLM's prompt window. It is the most critical factor in preventing hallucination.

---

## The "Need to Know" Principle

Just like human employees, Agents should only be given the information necessary to complete their specific task.

* **Bad Context:** Giving the Fact Checker the entire conversational history, the Planner's scratchpad, and the user's billing tier. (High cost, high distraction).
* **Good Context:** Giving the Fact Checker *only* the single claim it needs to check, and the specific reference document to check it against.

## Context Density vs. Length

LLMs suffer from the "Lost in the Middle" phenomenon. If you provide 100 pages of text, they will remember the beginning and the end, but forget the middle.

**Engineering Solutions:**
1. **Extraction over Inclusion:** Instead of putting the whole website HTML in the prompt, use a lightweight tool (e.g., BeautifulSoup) to extract just the `<p>` tags before it ever hits the LLM.
2. **Re-ranking:** When retrieving documents from vector storage, use a Re-ranker model (like Cohere Re-rank) to put the most definitively relevant chunks at the very top of the context window.

## XML Tagging for Structural Context

LLMs parse structured text better than raw blobs. In Nexus, we wrap injected context in XML-style tags within the prompt.

```xml
<user_request>
Analyze agentic architectures.
</user_request>

<evidence_to_synthesize>
<item id="1">Agents use tools.</item>
<item id="2">Agents use shared state.</item>
</evidence_to_synthesize>
```
This dramatically reduces instances of the LLM confusing the user's instructions with the research data.
