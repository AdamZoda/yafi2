import os
import sys
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_rag import EnhancedRAGSystem
from conversation_manager import conversation_manager

def test_single_rag():
    load_dotenv()
    rag = EnhancedRAGSystem()
    
    session_id = "debug_sess"
    query = "C'est quoi l'ENSA ?"
    
    # 1. Add user message
    conversation_manager.add_message(session_id, 'user', query)
    
    # 2. Try generate
    try:
        print("🚀 Calling generate_response...")
        res = rag.generate_response(query, session_id=session_id)
        print(f"✅ Success! Response length: {len(res.get('response', ''))}")
    except Exception as e:
        print(f"❌ CRASH: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_rag()
