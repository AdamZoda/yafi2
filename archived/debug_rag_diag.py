import sys
import os

# Ajout du chemin backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from vector_knowledge import VectorKnowledgeBase

def diag():
    kb = VectorKnowledgeBase()
    query = "Comment s'inscrire à la Fac ?"
    print(f"\nQUERY: {query}")
    
    results = kb.search(query, top_k=4, threshold=0.3)
    
    if not results:
        print("AUCUN RÉSULTAT")
        return

    print(f"\nTROUVÉ {len(results)} RÉSULTATS :")
    for i, res in enumerate(results):
        print(f"\n--- RÉSULTAT {i+1} (Score: {res['score']:.4f}) ---")
        print(f"CATEGORIE: {res['metadata'].get('category')}")
        print(f"TEXTE: {res['text'][:300]}...")

if __name__ == "__main__":
    diag()
