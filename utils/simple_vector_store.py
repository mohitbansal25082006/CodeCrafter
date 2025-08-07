# utils/simple_vector_store.py
import os
import json
import time
from utils.config import VECTOR_STORE_PATH

class SimpleVectorStore:
    def __init__(self):
        self.snippets = {}
        self.load_snippets()
    
    def load_snippets(self):
        """Load snippets from file if it exists."""
        try:
            if os.path.exists(VECTOR_STORE_PATH):
                with open(VECTOR_STORE_PATH, 'r') as f:
                    self.snippets = json.load(f)
        except Exception as e:
            print(f"Error loading snippets: {e}")
            self.snippets = {}
    
    def save_snippets(self):
        """Save snippets to file."""
        try:
            with open(VECTOR_STORE_PATH, 'w') as f:
                json.dump(self.snippets, f)
        except Exception as e:
            print(f"Error saving snippets: {e}")
    
    def add_snippet(self, snippet_id, code, metadata=None):
        """Add a code snippet to the store."""
        if metadata is None:
            metadata = {}
        # Ensure required metadata fields
        metadata.setdefault("language", "unknown")
        metadata.setdefault("task", "unknown")
        metadata.setdefault("timestamp", str(time.time()))
        
        self.snippets[snippet_id] = {
            "code": code,
            "metadata": metadata
        }
        self.save_snippets()
    
    def search_snippets(self, query, n_results=5):
        """Search for similar code snippets (simple keyword search)."""
        query_lower = query.lower()
        results = {
            "documents": [],
            "metadatas": [],
            "ids": []
        }
        
        # Simple keyword matching
        for snippet_id, snippet_data in self.snippets.items():
            code = snippet_data["code"]
            metadata = snippet_data["metadata"]
            
            # Check if query is in code or metadata
            if (query_lower in code.lower() or 
                query_lower in metadata.get("task", "").lower() or
                query_lower in metadata.get("language", "").lower()):
                
                results["documents"].append(code)
                results["metadatas"].append(metadata)
                results["ids"].append(snippet_id)
                
                # Limit results
                if len(results["documents"]) >= n_results:
                    break
        
        return results
    
    def get_snippet_by_id(self, snippet_id):
        """Retrieve a specific snippet by its ID."""
        if snippet_id in self.snippets:
            return {
                "documents": [self.snippets[snippet_id]["code"]],
                "metadatas": [self.snippets[snippet_id]["metadata"]],
                "ids": [snippet_id]
            }
        return {"documents": [], "metadatas": [], "ids": []}

# Initialize the vector store
vector_store = SimpleVectorStore()