import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import server_optimized
from server_optimized import app
import enhanced_rag

print("--- AGENTIC FUSION TEST (6-ARG EXPERT) ---")

with patch('server_optimized.is_ollama_available', return_value=True):
    with patch.object(enhanced_rag.rag_system, 'generate_response') as mock_gen:
        # Include moyenne in the tag as per new instructions
        mock_gen.return_value = {
            "response": "Certainement ! Je peux évaluer ton dossier. Basé sur tes informations : [PROLOG_EVALUATE: bac=PC, moyenne=15.5, budget=30000, ville=Rabat, ecole=ENSA]",
            "method": "mocked_ollama"
        }
        
        client = app.test_client()
        
        test_msg = "Je veux calculer mon score pour l'ENSA. J'ai un bac PC, 15.5 de moyenne, mon budget est de 30000 DH et j'habite à Rabat."
        print(f"User Message: {test_msg}")
        
        response = client.post('/chat', json={
            "message": test_msg,
            "session_id": "test_agentic_6arg"
        })
        
        data = response.get_json()
        print("\n--- FINAL RESPONSE (Expert Verdict Expected) ---")
        print(data.get('response'))
        print("\n--- METADATA ---")
        print(f"Source: {data.get('source') if data else 'None'}")

print("\n✓ Test complete. If you see a score and 'Verdict de l'Expert Prolog', the 6-arg integration is success!")
