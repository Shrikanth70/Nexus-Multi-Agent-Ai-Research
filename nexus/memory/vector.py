import os
import chromadb
from typing import List, Dict, Any
from nexus.config import settings
from nexus.observability.logger import get_logger

logger = get_logger(__name__)

class VectorMemory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorMemory, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # We store chroma DB inside the project root under a .chroma folder
        self.persist_directory = os.path.join(os.getcwd(), ".chroma")
        os.makedirs(self.persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # We use a default collection named "nexus_memory"
        self.collection = self.client.get_or_create_collection(name="nexus_memory")
        logger.info(f"Initialized VectorMemory at {self.persist_directory}")

    def store_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Store documents into ChromaDB.
        documents: List of text chunks
        metadatas: List of dictionaries (e.g. source URL, title)
        ids: Unique identifiers for the chunks
        """
        if not documents:
            return
            
        logger.info(f"Storing {len(documents)} documents into VectorMemory.")
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            logger.error(f"Failed to store documents in VectorMemory: {str(e)}")

    def search_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for top k most relevant documents.
        """
        logger.info(f"Searching VectorMemory for: {query}")
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            # Reformat results into a friendly list of dicts
            formatted_results = []
            if results and 'documents' in results and results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    doc = results['documents'][0][i]
                    meta = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    formatted_results.append({
                        "text": doc,
                        "metadata": meta
                    })
            return formatted_results
        except Exception as e:
            logger.error(f"VectorMemory search failed: {str(e)}")
            return []

vector_memory = VectorMemory()
