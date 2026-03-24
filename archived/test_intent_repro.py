
import sys
import os

# Mocking Flask request for local testing
class MockRequest:
    def __init__(self, json_data):
        self.json = json_data

# Mocking jsonify
def jsonify(data):
    return data

# We need to import the logic from server.py or simulate it
# Since server.py is complex, I will copy the critical parts of chat() into a test script

sys.path.append(r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend')
from intent_classifier import IntentClassifier

classifier = IntentClassifier()

def test_query(msg):
    print(f"\n--- Testing Query: '{msg}' ---")
    msg_low = msg.lower()
    # Basic normalization as in server.py
    import unicodedata
    msg_norm = ''.join(c for c in unicodedata.normalize('NFD', msg_low) if unicodedata.category(c) != 'Mn')
    
    intent = classifier.classify(msg_norm, threshold=0.60)
    print(f"Detected Intent: {intent}")
    
    # Simulate the check for schools in COMPARE_SCHOOLS
    KNOWN_ENTITIES = [
        "emsi", "uir", "um6p", "ensa", "encg", "fst", "ensias", "iscae", "uic", "fmp",
        "ensam", "ensck", "isss", "ispits", "enam", "iav", "ispm", "itsat", "isic", "inau",
        "isadac", "esba", "inba", "insap", "aat", "isitt", "imsk", "iss", "issf", "irfcjs", "ena",
        "ofppt", "medecine", "pharmacie", "architecture", "minhaty",
        "casablanca", "rabat", "marrakech", "tanger", "agadir", "fes"
    ]
    
    schools_in_msg = []
    for ent in KNOWN_ENTITIES:
        if ent in msg_low:
            schools_in_msg.append(ent)
    
    print(f"Schools detected: {schools_in_msg}")
    
    if intent == "COMPARE_SCHOOLS":
        if len(schools_in_msg) >= 2:
            print("Action: Would perform side-by-side comparison.")
        else:
            print("Action: Would ask for two schools.")

test_queries = [
    "Comparer EMSI et UIR (Salaires & Débouchés)",
    "Différence entre ENSA et ENAM ?",
    "Quelle est la différence entre ENSA et FST ?"
]

for q in test_queries:
    test_query(q)
