import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class RetrievalService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_path: str = "faiss_index.bin", metadata_path: str = "metadata.pkl"):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.index = None
        self.chunks = [] # Metadata storage (simple list for now)
        
        self.load_index()

    def create_embedding(self, text: str) -> np.ndarray:
        return self.model.encode([text])[0]

    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

    def add_documents(self, chunks: List[str]):
        """Adds text chunks to the FAISS index."""
        if not chunks:
            return
        
        embeddings = self.create_embeddings(chunks)
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
            
        self.index.add(np.array(embeddings).astype('float32'))
        self.chunks.extend(chunks)
        self.save_index()

    def search(self, query: str, k: int = 3) -> List[str]:
        """Searches for the top-k most similar chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = self.create_embedding(query)
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), k)
        
        results = []
        seen_chunks = set()
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                chunk_text = self.chunks[idx]
                if chunk_text not in seen_chunks:
                    results.append(chunk_text)
                    seen_chunks.add(chunk_text)
                
        return results

    def save_index(self):
        if self.index:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.chunks, f)

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.chunks = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.chunks = []

if __name__ == "__main__":
    # Test
    retriever = RetrievalService()
    print("Retrieval Service Initialized")
