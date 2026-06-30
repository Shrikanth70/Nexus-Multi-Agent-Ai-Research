import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_chroma():
    with patch("nexus.memory.vector.chromadb.PersistentClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_collection = MagicMock()
        mock_instance.get_or_create_collection.return_value = mock_collection
        yield mock_collection

@pytest.mark.unit
def test_vector_memory_store(mock_chroma):
    from nexus.memory.vector import VectorMemory
    # Clear the singleton instance for testing
    VectorMemory._instance = None
    vm = VectorMemory()
    
    docs = ["doc1", "doc2"]
    metas = [{"url": "url1"}, {"url": "url2"}]
    ids = ["id1", "id2"]
    
    vm.store_documents(docs, metas, ids)
    mock_chroma.add.assert_called_once_with(documents=docs, metadatas=metas, ids=ids)

@pytest.mark.unit
def test_vector_memory_search(mock_chroma):
    from nexus.memory.vector import VectorMemory
    VectorMemory._instance = None
    vm = VectorMemory()
    
    mock_chroma.query.return_value = {
        "documents": [["result doc"]],
        "metadatas": [[{"url": "result url"}]]
    }
    
    results = vm.search_documents("query", k=1)
    
    assert len(results) == 1
    assert results[0]["text"] == "result doc"
    assert results[0]["metadata"]["url"] == "result url"
