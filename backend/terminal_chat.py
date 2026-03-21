import sys
import os
import json
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_rag import EnhancedRAGSystem
from llm_engine import llm_engine

def chat_loop():
    load_dotenv()
    print("🚀 INITIALIZING YAFI TERMINAL CHAT...")
    rag = EnhancedRAGSystem()
    
    print("\n--- BIENVENUE SUR YAFI (VERSION TERMINAL) ---")
    print("Tape 'exit' pour quitter.\n")
    
    # Mock profile
    profile = {
        "id": "terminal_user",
        "name": "TESTEUR USER",
        "is_premium": True
    }
    
    while True:
        user_input = input("\n👤 VOUS: ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
            
        print("🤖 RÉFLEXION...")
        
        # 1. Simulate server logic
        try:
            result = rag.generate_response(user_input, profile=profile)
            response = result.get("response", "Désolé, je ne sais pas répondre.")
            method = result.get("method", "pures_rag")
            
            print(f"\n✨ YAFI ({method}):")
            print(f"----------------------------------------")
            print(response)
            print(f"----------------------------------------")
            
        except Exception as e:
            print(f"❌ ERREUR: {e}")

if __name__ == "__main__":
    chat_loop()
