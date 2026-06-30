from typing import List, Dict
from duckduckgo_search import DDGS
from nexus.observability.logger import get_logger

logger = get_logger(__name__)

def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web using DuckDuckGo.
    Returns a list of dictionaries with 'title', 'link', and 'snippet'.
    """
    logger.info(f"Searching web for: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            # text() returns an iterator of dicts
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        logger.error(f"Web search failed: {str(e)}")
        
    return results
