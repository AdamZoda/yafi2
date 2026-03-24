"""
New RAG Knowledge Base with Vector Search
Replaces the old TF-IDF approach with semantic embeddings
"""

import os
from typing import Optional, Dict, List
from embedding_service import EmbeddingService


class VectorKnowledgeBase:
    """Vector-based knowledge base using FAISS and sentence transformers"""
    
    def __init__(self, chunks_file: str = None, index_file: str = None):
        """
        Initialize the vector knowledge base
        
        Args:
            chunks_file: Path to knowledge_chunks.json
            index_file: Path to FAISS index file
        """
        # Default paths
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        self.chunks_file = chunks_file or os.path.join(backend_dir, 'knowledge_chunks.json')
        self.index_file = index_file or os.path.join(backend_dir, 'yafi_vector_index.faiss')
        
        # Initialize embedding service
        self.service = EmbeddingService()
        
        # Load index if exists
        if os.path.exists(self.index_file) and os.path.exists(self.chunks_file):
<<<<<<< HEAD
            print(f"📂 Loading vector index from: {self.index_file}")
            self.service.load_index(self.index_file, self.chunks_file)
            print(f"✅ Vector knowledge base ready ({self.service.index.ntotal} vectors)")
        else:
            print(f"⚠️ Vector index not found. Run build_vector_index.py first.")
=======
            print(f"Loading vector index from: {self.index_file}")
            self.service.load_index(self.index_file, self.chunks_file)
            print(f"Vector knowledge base ready ({self.service.index.ntotal} vectors)")
        else:
            print(f"Vector index not found. Run build_vector_index.py first.")
>>>>>>> 3257fc1 (final)
            self.service = None
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.6) -> Optional[List[Dict]]:
        """
        Perform semantic search on the knowledge base
        
        Args:
            query: User query
            top_k: Number of results to return
            threshold: Minimum similarity score (0-1)
            
        Returns:
            List of results with chunks and scores, or None
        """
        if not self.service:
<<<<<<< HEAD
            print("⚠️ Vector search not available")
=======
            print("Vector search not available")
>>>>>>> 3257fc1 (final)
            return None
        
        try:
            results = self.service.search(query, top_k=top_k, threshold=threshold)
            return results
        except Exception as e:
<<<<<<< HEAD
            print(f"❌ Error during vector search: {e}")
=======
            print(f"Error during vector search: {e}")
>>>>>>> 3257fc1 (final)
            return None
    
    def find_best_match(self, user_query: str, threshold: float = 0.6) -> Optional[Dict]:
        """
        Find the best matching answer for a user query
        
        Args:
            user_query: User's question
            threshold: Minimum confidence score
            
        Returns:
            Dict with 'question', 'answer', 'category', 'score' or None
        """
        results = self.search(user_query, top_k=3, threshold=threshold)
        
        if not results:
            return None
        
        # Return the top result
        best = results[0]
        
        return {
            'question': best['metadata'].get('question', ''),
            'answer': best['text'],
            'category': best['metadata'].get('category', 'Général'),
            'score': best['score']
        }
    
    def get_context_for_llm(self, query: str, top_k: int = 3) -> str:
        """
        Get formatted context for LLM prompting
        
        Args:
            query: User query
            top_k: Number of context chunks to retrieve
            
        Returns:
            Formatted context string
        """
        results = self.search(query, top_k=top_k, threshold=0.5)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            category = result['metadata'].get('category', 'Général')
            text = result['text']
            score = result['score']
            
            context_parts.append(
                f"[Source {i} - {category} - Score: {score:.2f}]\n{text}\n"
            )
        
        return "\n---\n".join(context_parts)


# Fallback: Keep old RAG for compatibility
class LegacyRAGKnowledge:
    """Legacy TF-IDF based knowledge (fallback)"""
    
    def __init__(self):
<<<<<<< HEAD
        print("⚠️ Using legacy TF-IDF knowledge base (fallback)")
=======
        print("Using legacy TF-IDF knowledge base (fallback)")
>>>>>>> 3257fc1 (final)
        # Import old implementation if needed
        from rag_knowledge import YAFIKnowledgeBase
        self.kb = YAFIKnowledgeBase()
    
    def find_best_match(self, user_query: str, threshold: float = 0.5):
        return self.kb.find_best_match(user_query, threshold)


if __name__ == "__main__":
    # Test the vector knowledge base
    print("🧪 Testing Vector Knowledge Base\n")
    
    kb = VectorKnowledgeBase()
    
    if kb.service:
        # Test queries
        test_queries = [
            "C'est quoi l'ENSA ?",
            "Comment s'inscrire à la fac ?",
            "Quels sont les débouchés pour un Bac SVT ?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            result = kb.find_best_match(query, threshold=0.5)
            
            if result:
                print(f"   ✅ Match found (score: {result['score']:.3f})")
                print(f"   Category: {result['category']}")
                print(f"   Answer: {result['answer'][:100]}...")
            else:
                print(f"   ❌ No match found")
