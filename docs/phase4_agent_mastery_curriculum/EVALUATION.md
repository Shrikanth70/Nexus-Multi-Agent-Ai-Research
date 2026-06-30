# 📈 Evaluation
## Nexus Research Intelligence Platform

> **Status:** Discovery
> **Phase:** 4 - Agent Mastery Curriculum

You cannot improve what you cannot measure. Because AI outputs are non-deterministic, traditional unit tests (asserting exact string matches) are useless. We must build an Evaluation Pipeline.

---

## 1. The "LLM-as-a-Judge" Pattern

We use a highly capable model (like GPT-4) to evaluate the output of our specialized agents (which might be running cheaper models).

### The Rubric
We provide the Judge model with a strict scoring rubric.
* **Prompt to Judge:** "Review the following `DraftReport`. Score it from 1-5 on: 1. Factual accuracy based on the provided evidence. 2. Tone matching the enterprise guidelines. 3. Absence of hallucination."

## 2. Building the Golden Dataset

To measure progress, we need a static dataset of test cases.
* **Dataset:** 50 diverse research queries (e.g., "History of AI", "Comparison of SQL vs NoSQL", "Summary of Quantum Physics").
* Every time we change a prompt or a tool in Nexus, we run the entire dataset through the workflow.
* We compare the Judge's aggregate score (e.g., 85/100) to the previous version (82/100). If the score goes down, the PR is rejected.

## 3. Metrics to Track

Beyond just quality scores, an enterprise system must evaluate:
* **Token Usage:** Did the new prompt cause the agent to use 2x more tokens?
* **Latency:** Did the new parallel workflow actually speed up the total response time?
* **Tool Failure Rate:** How often did the Web Search tool return an error that the agent had to recover from?
* **Loop Count:** How many times did the Fact Checker reject the Researcher on average? (High loop counts indicate bad instructions).
