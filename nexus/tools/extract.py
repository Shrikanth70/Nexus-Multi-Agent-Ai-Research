from typing import Optional
from playwright.sync_api import sync_playwright
from unstructured.partition.html import partition_html
from nexus.observability.logger import get_logger

logger = get_logger(__name__)

def scrape_url(url: str) -> Optional[str]:
    """
    Scrape a URL using Playwright and parse with unstructured.
    Returns the cleaned text content.
    """
    logger.info(f"Scraping URL: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            html_content = page.content()
            browser.close()
            
            elements = partition_html(text=html_content)
            clean_text = "\n\n".join([str(e) for e in elements])
            return clean_text
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {str(e)}")
        return None
