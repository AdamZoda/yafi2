import unittest
from unittest.mock import patch, MagicMock
import json

# Mocking Flask and other dependencies before importing server_optimized
import sys
from unittest.mock import MagicMock

sys.modules['flask'] = MagicMock()
sys.modules['flask_cors'] = MagicMock()
sys.modules['pyswip'] = MagicMock()
sys.modules['conversation_manager'] = MagicMock()
sys.modules['vector_knowledge'] = MagicMock()
sys.modules['response_builder'] = MagicMock()
sys.modules['llm_engine'] = MagicMock()
sys.modules['enhanced_rag'] = MagicMock()
sys.modules['intent_classifier'] = MagicMock()

# Now we can import the extractor and test it
from backend.entity_extractor import EntityExtractor

class TestEntityExtraction(unittest.TestCase):
    @patch('backend.entity_extractor.llm_engine')
    def test_extraction_logic(self, mock_llm):
        # Setup mock
        mock_llm.ask.return_value = json.dumps({
            "bac": "PC",
            "moyenne": 15.5,
            "budget": 30000,
            "ville": "Rabat",
            "ecole": "ENSA"
        })
        
        extractor = EntityExtractor()
        res = extractor.extract("Je suis en PC avec 15.5 de moyenne à Rabat pour l'ENSA")
        
        print(f"Extracted: {res}")
        self.assertEqual(res['bac'], "PC")
        self.assertEqual(res['moyenne'], 15.5)
        self.assertEqual(res['ville'], "Rabat")
        self.assertEqual(res['ecole'], "ENSA")

    @patch('backend.entity_extractor.llm_engine')
    def test_extraction_missing(self, mock_llm):
        # Setup mock with missing fields
        mock_llm.ask.return_value = json.dumps({
            "bac": None,
            "moyenne": None,
            "budget": 20000,
            "ville": "casablanca",
            "ecole": "ENCG"
        })
        
        extractor = EntityExtractor()
        res = extractor.extract("Budget 20k pour ENCG à Casa")
        
        print(f"Extracted (Missing): {res}")
        self.assertEqual(res['budget'], 20000)
        self.assertEqual(res['ville'], "Casablanca")
        self.assertEqual(res['ecole'], "ENCG")
        self.assertIsNone(res['bac'])

if __name__ == "__main__":
    unittest.main()
