import os
import sys
from dotenv import load_dotenv

# Add current dir to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_rag import EnhancedRAGSystem
    from llm_engine import llm_engine
    print("✅ Imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def run_tests():
    load_dotenv()
    
    print("\n--- INITIALIZING SYSTEM ---")
    rag = EnhancedRAGSystem()
    
    test_queries = [
        "quels sont les débouchés pour un bac svt ?",
        "comment s'inscrire à la fac ?",
        "date du concours ensa ?",
        "c'est quoi l'encg ?",
        "bts ou dut ?",
        "Quasiment impossible d'entrer en médecine sans mention ?" # Test complexité
    ]
    
    print(f"\n--- RUNNING {len(test_queries)} TESTS ---")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nPROMPT {i}: '{query}'")
        print("-" * 50)
        
        # Test Phase 2 (RAG + LLM)
        try:
            result = rag.generate_response(query, use_llm=True)
            response = result.get("response", "")
            method = result.get("method", "unknown")
            confidence = result.get("confidence", 0.0)
            
            if response:
                print(f"🤖 RESPONSE (Method: {method}):")
                print(f"   {response[:300]}...")
            else:
                print("⚠️ No response from RAG/LLM.")
        except Exception as e:
            print(f"❌ RAG Error: {e}")

if __name__ == "__main__":
    run_tests()
