import pytest
from unittest.mock import patch, MagicMock
from nexus.tools.search import web_search
from nexus.tools.extract import scrape_url

@pytest.mark.unit
@patch("nexus.tools.search.DDGS")
def test_web_search(mock_ddgs):
    mock_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_instance
    mock_instance.text.return_value = [
        {"title": "Test Title", "href": "http://test.com", "body": "Test snippet"}
    ]
    
    results = web_search("test query", max_results=1)
    
    assert len(results) == 1
    assert results[0]["title"] == "Test Title"
    assert results[0]["link"] == "http://test.com"
    assert results[0]["snippet"] == "Test snippet"


@pytest.mark.unit
@patch("nexus.tools.extract.sync_playwright")
@patch("nexus.tools.extract.partition_html")
def test_scrape_url(mock_partition, mock_playwright):
    mock_pw_instance = MagicMock()
    mock_playwright.return_value.__enter__.return_value = mock_pw_instance
    
    mock_browser = MagicMock()
    mock_pw_instance.chromium.launch.return_value = mock_browser
    
    mock_page = MagicMock()
    mock_browser.new_page.return_value = mock_page
    mock_page.content.return_value = "<html><body>Test</body></html>"
    
    # Mock partition_html returning a list of elements
    mock_element = MagicMock()
    mock_element.__str__.return_value = "Test Content"
    mock_partition.return_value = [mock_element]
    
    result = scrape_url("http://test.com")
    
    assert result == "Test Content"
    mock_page.goto.assert_called_with("http://test.com", wait_until="domcontentloaded", timeout=15000)
