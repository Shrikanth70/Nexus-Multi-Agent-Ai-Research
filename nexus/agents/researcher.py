"""
Researcher Agent.

Uses LLM to execute research tasks and generate findings (evidence).
"""

import hashlib
from typing import List
import structlog
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from nexus.agents.base import BaseAgent
from nexus.core.state import AgentName, Evidence, NexusState, TaskStatus, AgentOutput
from nexus.prompts.system_prompts import RESEARCHER_PROMPT

logger = structlog.get_logger(__name__)

# Import our new tools and memory
from nexus.tools.search import web_search
from nexus.tools.extract import scrape_url
from nexus.memory.vector import vector_memory


class SearchQueryOutput(BaseModel):
    """Output for generating an optimal search query."""
    query: str = Field(description="The optimal search engine query to find information for the task.")


class FindingsOutput(BaseModel):
    """Structured output expected from the Researcher LLM."""
    findings: List[Evidence] = Field(description="The evidence gathered for the pending tasks.")


class ResearcherAgent(BaseAgent):
    """
    Executes tasks and generates evidence using RAG and Web Search.
    """
    
    @property
    def name(self) -> AgentName:
        return AgentName.RESEARCHER
        
    def execute(self, state: NexusState) -> AgentOutput:
        logger.info(f"{self.name.value} executing...", session_id=state.session_id)
        logs = []
        
        pending_tasks = [t for t in state.plan.tasks if t.status == TaskStatus.PENDING]
        
        if pending_tasks:
            # We process one task at a time to keep LLM context focused
            current_task = pending_tasks[0]
            logger.info(f"Researching task: {current_task.id}")
            logs.append(f"Researching task: {current_task.id}")
            
            # 1. Generate optimal search query
            query_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert researcher. Given a task and the original user query, output the single best search engine query to find relevant factual information. Keep it concise, keywords only."),
                ("user", "Original Query: {query}\nTask: {task_desc}")
            ])
            query_chain = query_prompt | self.llm.with_structured_output(SearchQueryOutput)
            query_result: SearchQueryOutput = query_chain.invoke({ # type: ignore
                "query": state.user_query,
                "task_desc": current_task.description
            })
            search_query = query_result.query
            logger.info(f"Generated search query: {search_query}")

            # 2. Search DuckDuckGo
            search_results = web_search(search_query, max_results=3)
            
            docs = []
            metadatas = []
            ids = []
            
            # 3. Scrape URLs and prep for Vector DB
            for res in search_results:
                url = res.get("link")
                if url:
                    content = scrape_url(url)
                    if content and len(content) > 100:
                        # Chunk it simply (first 4000 chars for now to fit in prompt limits)
                        content_chunk = content[:4000]
                        docs.append(content_chunk)
                        metadatas.append({"url": url, "title": res.get("title", "")})
                        ids.append(hashlib.md5(url.encode()).hexdigest())

            # 4. Store extracted chunks in Vector DB
            if docs:
                vector_memory.store_documents(documents=docs, metadatas=metadatas, ids=ids)

            # 5. Retrieve Context (Top 2 most semantic results)
            context_results = vector_memory.search_documents(search_query, k=2)
            if context_results:
                context_text = "\n\n---\n\n".join([f"Source: {c['metadata'].get('url')}\nContent: {c['text']}" for c in context_results])
            else:
                context_text = "No context found from web search."

            # 6. Generate Findings based on Context
            prompt = ChatPromptTemplate.from_messages([
                ("system", RESEARCHER_PROMPT),
                ("user", "User Query: {query}\n\nTask to execute: {task_desc}\n\nRetrieved Context:\n{context}")
            ])
            
            chain = prompt | self.llm.with_structured_output(FindingsOutput)
            
            result: FindingsOutput = chain.invoke({ # type: ignore
                "query": state.user_query,
                "task_desc": current_task.description,
                "context": context_text
            })
            
            # Update state
            current_task.status = TaskStatus.COMPLETED
            current_task.result = f"Evidence generated from web search ({len(search_results)} sources checked)."
            
            # Ensure task_id is correctly mapped on new evidence
            for ev in result.findings:
                ev.task_id = current_task.id
                state.evidence.append(ev)
            
            # Check if more tasks remain
            has_more = any(t.status == TaskStatus.PENDING for t in state.plan.tasks)
            state.current_agent = AgentName.RESEARCHER if has_more else AgentName.FACT_CHECKER
            
        else:
            state.current_agent = AgentName.FACT_CHECKER
            
        return AgentOutput(
            agent=self.name.value,
            status="success",
            data=state.model_dump(),
            logs=logs
        )
