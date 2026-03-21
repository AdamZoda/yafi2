import unittest
from unittest.mock import patch, MagicMock
import json
import re
import sys
import traceback

# Define a pass-through decorator to preserve the original function
def mock_route(path, **kwargs):
    def decorator(f):
        return f
    return decorator

# Mocking all dependencies
mock_flask = MagicMock()
mock_flask.Flask.return_value.route = mock_route
sys.modules['flask'] = mock_flask
sys.modules['flask_cors'] = MagicMock()
sys.modules['pyswip'] = MagicMock()
sys.modules['conversation_manager'] = MagicMock()
sys.modules['vector_knowledge'] = MagicMock()
sys.modules['response_builder'] = MagicMock()
sys.modules['llm_engine'] = MagicMock()
sys.modules['enhanced_rag'] = MagicMock()
sys.modules['intent_classifier'] = MagicMock()
sys.modules['entity_extractor'] = MagicMock()

import backend.server_optimized as server

class TestFullNLPFlow(unittest.TestCase):
    @patch('backend.server_optimized.entity_extractor')
    @patch('backend.server_optimized.rag_system')
    @patch('backend.server_optimized.prolog')
    @patch('backend.server_optimized.is_ollama_available')
    def test_end_to_end_extraction_merging(self, mock_available, mock_prolog, mock_rag, mock_extractor):
        mock_available.return_value = True
        
        # 1. Mock Entity Extractor (Pre-extraction)
        mock_extractor.extract.return_value = {
            "bac": "PC",
            "moyenne": 15.5,
            "budget": 30000,
            "ville": "Rabat",
            "ecole": None 
        }
        
        # 2. Mock RAG/Ollama
        mock_rag.generate_response.return_value = {
            "response": "Je vais calculer pour l'ENSA. [PROLOG_EVALUATE: ecole=ENSA]"
        }
        
        # 3. Mock Prolog Query
        mock_prolog.query.return_value = [{"Score": 61.0}]
        
        # Mock request and jsonify
        with patch('backend.server_optimized.request') as mock_request:
            mock_request.json = {"message": "Je suis en PC 15.5 à Rabat, quel est mon score pour l'ENSA?", "session_id": "test"}
            
            with patch('backend.server_optimized.jsonify') as mock_jsonify:
                try:
                    print(f"🔍 DEBUG: server.chat identity: {server.chat}")
                    print("🚀 Calling server.chat()...")
                    sys.stdout.flush()
                    server.chat()
                    print("🏁 server.chat() returned.")
                except Exception as e:
                    print(f"❌ chat() raised exception: {e}")
                    traceback.print_exc()
                
                # Verify Prolog call arguments
                if mock_prolog.query.call_args:
                    args = mock_prolog.query.call_args[0][0]
                    print(f"Prolog Query Generated: {args}")
                    
                    self.assertIn("'PC'", args)
                    self.assertIn("15.5", args)
                    self.assertIn("'Rabat'", args)
                    self.assertIn("'ENSA'", args)
                else:
                    self.fail("prolog.query() was never called!")
                
                # Check response
                if mock_jsonify.call_args:
                    response_data = mock_jsonify.call_args[0][0].get('response', '')
                    print(f"Final Response: {response_data}")
                    self.assertIn("61.0%", response_data)
                else:
                    self.fail("jsonify() was never called!")

if __name__ == "__main__":
    unittest.main()
