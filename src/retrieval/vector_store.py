import faiss
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import logging

logger = logging.getLogger(__name__)

class FAISSStore:
    def __init__(self, index_path: str = "data/index/faiss.index", model_name: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.metadata = []
        self.content = []
        
        if os.path.exists(self.index_path):
            self.load()
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def add(self, chunks: list, batch_size: int = 16):
        if not chunks: return
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            contents = [chunk['content'] for chunk in batch]
            embeddings = self.model.encode(contents, show_progress_bar=False)
            self.index.add(np.array(embeddings).astype('float32'))
            self.metadata.extend([chunk['metadata'] for chunk in batch])
            self.content.extend(contents)
        
        self.save()

    def search(self, query: str, k: int = 4):
        if self.index.ntotal == 0: return []
        query_embedding = self.model.encode([query], show_progress_bar=False)
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.content):
                results.append({
                    'content': self.content[idx],
                    'metadata': self.metadata[idx],
                    'distance': float(distances[0][i])
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(f"{self.index_path}.data", 'wb') as f:
            pickle.dump({'metadata': self.metadata, 'content': self.content}, f)

    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(f"{self.index_path}.data", 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.content = data['content']
