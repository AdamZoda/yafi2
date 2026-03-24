import os
import sys
import json

# Add backend to path
backend_dir = r"c:\Users\PC\Downloads\YAFI\yafi2-main\backend"
sys.path.append(backend_dir)

from embedding_service import EmbeddingService

def test_rag():
    service = EmbeddingService()
    
    # Check if index exists
    index_path = os.path.join(backend_dir, "yafi_vector_index.faiss")
    if not os.path.exists(index_path):
        print(f"Error: Index not found at {index_path}")
        return

    query = "C'est quoi l'OFPPT ?"
    print(f"Testing query: {query}")
    
    # Try different thresholds
    for threshold in [0.3, 0.4, 0.5, 0.6]:
        print(f"\nSearching with threshold: {threshold}")
        results = service.search(query, top_k=3, threshold=threshold)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, res in enumerate(results):
                print(f"  [{i+1}] Score: {res['score']:.3f} | {res['text'][:100]}...")
        else:
            print("No results found.")

if __name__ == "__main__":
    test_rag()
