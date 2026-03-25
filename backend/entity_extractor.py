import json
import re
from llm_engine import llm_engine

EXTRACTION_PROMPT = """
Tu es un expert en extraction d'entités pour un système d'orientation scolaire au Maroc (YAFI).
Extrais les entités du message de l'utilisateur suivant au format JSON uniquement.

Entités à extraire (si présentes) :
- bac: La série du baccalauréat (ex: PC, SVT, SM, ECO, LITT, TECH). 
- moyenne: La note du bac ou moyenne générale (Nombre décimal, ex: 15.5).
- budget: Le budget annuel maximum en DH (Nombre entier, ex: 30000).
- ville: La ville de résidence ou la ville cible (Nom propre, ex: 'Rabat').
- ecole: Le sigle de l'école ou le type de formation visée (ex: 'ENSA', 'ENCG', 'Medecine', 'FST', 'Droit').

Règles de normalisation :
1. Réponds UNIQUEMENT avec le JSON. Pas de texte avant ou après.
2. Si une entité est totalement absente du message, mets null.
3. Pour 'ecole', utilise le sigle standard (ex: 'ENSA' au lieu de 'Ecole Nationale des Sciences Appliquées').
4. Pour 'ville', capitalise la première lettre (ex: 'Casablanca').

Message : "{user_message}"
JSON:
"""

class EntityExtractor:
    def __init__(self):
        self.engine = llm_engine

    def extract(self, user_message: str) -> dict:
        """
        Extract entities from user message using LLM
        """
        prompt = EXTRACTION_PROMPT.format(user_message=user_message)
        
        try:
            # Call Ollama with JSON format support
            response = self.engine.ask(prompt, temperature=0.0, format="json")
            
            if not response:
                return {}
                
            # Parse JSON response
            extracted = json.loads(response)
            
            # Additional Sanitization
            sanitized = {
                "bac": str(extracted.get("bac")).upper() if extracted.get("bac") else None,
                "moyenne": self._to_float(extracted.get("moyenne")),
                "budget": self._to_int(extracted.get("budget")),
                "ville": str(extracted.get("ville")).capitalize() if extracted.get("ville") else None,
                "ecole": str(extracted.get("ecole")).upper() if extracted.get("ecole") else None
            }
            
            return sanitized
            
        except Exception as e:
            print(f"Entity Extraction Error: {e}")
            return {}

    def _to_float(self, val):
        if val is None: return None
        try: 
            # Handle cases where LLM might return string with comma
            if isinstance(val, str):
                val = val.replace(',', '.')
            return float(val)
        except: return None

    def _to_int(self, val):
        if val is None: return None
        try: return int(float(val))
        except: return None

# Singleton
entity_extractor = EntityExtractor()
