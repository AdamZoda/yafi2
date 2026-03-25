"""
Embedding Service for YAFI RAG System
Handles text embeddings and FAISS vector search
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from typing import List, Dict, Optional, Tuple


class EmbeddingService:
    """Service for generating embeddings and performing semantic search"""
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        # Use shared model if possible
        from intent_classifier import get_shared_model
        self.model = get_shared_model(model_name)
        
        self.index = None
        self.chunks = []
        self.dimension = 384  # MiniLM-L12 embedding dimension
        
    def encode(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings to encode
            show_progress: Whether to show progress bar
            
        Returns:
            numpy array of embeddings
        """
        return self.model.encode(texts, show_progress_bar=show_progress, convert_to_numpy=True, normalize_embeddings=True)
    
    def build_index(self, chunks: List[Dict], save_path: str = None):
        """
        Build FAISS index from knowledge chunks
        """
        print(f"Building FAISS index from {len(chunks)} chunks...")
        
        self.chunks = chunks
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.encode(texts)
        
        # Create FAISS index (L2 distance)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Index built successfully with {self.index.ntotal} vectors")
        
        # Save if path provided
        if save_path:
            self.save_index(save_path)
    
    def save_index(self, index_path: str):
        """Save FAISS index to disk"""
        faiss.write_index(self.index, index_path)
        print(f"Index saved to: {index_path}")
    
    def load_index(self, index_path: str, chunks_path: str):
        """
        Load FAISS index and chunks from disk
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        if not os.path.exists(chunks_path):
            raise FileNotFoundError(f"Chunks file not found: {chunks_path}")
        
        print(f"Loading index from: {index_path}")
        self.index = faiss.read_index(index_path)
        
        print(f"Loading chunks from: {chunks_path}")
        with open(chunks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.chunks = data['chunks']
        
        print(f"Loaded {self.index.ntotal} vectors and {len(self.chunks)} chunks")
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.7) -> Optional[List[Dict]]:
        """
        Perform semantic search on the knowledge base
        """
        if self.index is None:
            raise ValueError("Index not built or loaded. Call build_index() or load_index() first.")
        
        # Generate query embedding
        query_embedding = self.encode([query], show_progress=False)
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Convert L2 distance to cosine similarity (approximate)
        similarities = 1 - (distances[0] / 4)
        similarities = np.clip(similarities, 0, 1)
        
        # Filter by threshold and build results
        results = []
        for idx, sim in zip(indices[0], similarities):
            if sim >= threshold and idx < len(self.chunks):
                results.append({
                    'chunk': self.chunks[idx],
                    'score': float(sim),
                    'text': self.chunks[idx]['text'],
                    'metadata': self.chunks[idx].get('metadata', {})
                })
        
        return results if results else None
    
    def get_stats(self) -> Dict:
        return {
            'total_vectors': self.index.ntotal if self.index else 0,
            'total_chunks': len(self.chunks),
            'dimension': self.dimension,
            'model': self.model.get_sentence_embedding_dimension()
        }


if __name__ == "__main__":
    service = EmbeddingService()
    test_texts = ["C'est quoi l'ENSA ?", "Comment s'inscrire à la faculté ?"]
    embeddings = service.encode(test_texts)
    print(f"Generated embeddings shape: {embeddings.shape}")
