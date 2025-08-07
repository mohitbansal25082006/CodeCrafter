# utils/vector_store.py
import chromadb
from chromadb.config import Settings
from utils.config import CHROMA_DB_PATH

class VectorStore:
    def __init__(self):
        # Create Chroma client with persistent storage
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        # Create or get collection
        self.collection = self.client.get_or_create_collection(name="code_snippets")
    
    def add_snippet(self, snippet_id, code, metadata=None):
        """Add a code snippet to the vector store."""
        if metadata is None:
            metadata = {}
        # Ensure required metadata fields
        metadata.setdefault("language", "unknown")
        metadata.setdefault("task", "unknown")
        metadata.setdefault("timestamp", "unknown")
        
        self.collection.add(
            documents=[code],
            metadatas=[metadata],
            ids=[snippet_id]
        )
    
    def search_snippets(self, query, n_results=5):
        """Search for similar code snippets."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def get_snippet_by_id(self, snippet_id):
        """Retrieve a specific snippet by its ID."""
        result = self.collection.get(ids=[snippet_id])
        return result

# Initialize the vector store
vector_store = VectorStore()