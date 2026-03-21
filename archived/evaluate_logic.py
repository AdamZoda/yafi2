import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/chat"

test_cases = [
    {
        "q": "Prix EMSI ?",
        "must_contain": ["35 000", "scolarite", "dh"],
        "label": "Frais EMSI"
    },
    {
        "q": "Procedure pour la bourse Minhaty ?",
        "must_contain": ["minhaty.ma", "demande"],
        "label": "Procedure Minhaty"
    },
    {
        "q": "Quelle est la difference entre ENSA et FST ?",
        "must_contain": ["ensa", "fst"],
        "label": "Comparaison ENSA/FST"
    },
    {
        "q": "Puis-je faire medecine avec un Bac Eco ?",
        "must_contain": ["non", "desole", "impossible", "incompatible"], 
        "label": "Logique Bac Eco -> Medecine"
    },
    {
        "q": "Ou se trouve l'ENSIAS ?",
        "must_contain": ["rabat"],
        "label": "Localisation ENSIAS"
    },
    {
        "q": "Quels sont les metiers de l'IA ?",
        "must_contain": ["intelligence artificielle", "data", "metier"],
        "label": "Metiers IA"
    },
    {
        "q": "Quel est le seuil de l'ENCG ?",
        "must_contain": ["encg", "seuil"],
        "label": "Seuil ENCG"
    },
    {
        "q": "Quelles sont les conditions de bourse de merite a l'UIR ?",
        "must_contain": ["bourse", "uir", "merite"],
        "label": "Bourse UIR"
    },
    {
        "q": "Prix des ecoles de commerce privees ?",
        "must_contain": ["prix", "commerce", "dh"],
        "label": "Prix Commerce"
    },
    {
        "q": "Je suis perdu, conseille-moi une strategie",
        "must_contain": ["aider", "questions", "bac"],
        "label": "Orientation Quiz Start"
    },
    {
        "q": "Où étudier l'architecture ?",
        "must_contain": ["ville", "localisation", "Architecture", "où", "precisez"],
        "label": "Architecture Location (Not IA)"
    },
    {
        "q": "L'ingénierie est-elle un métier d'avenir ?",
        "must_contain": ["metiers", "avenir", "demande"],
        "label": "Ingenierie Jobs (Not specific IA but general jobs)"
    },
    {
        "q": "Quelle est la difference entre IA et Architecture ?",
        "must_contain": ["compar", "difference", "seuils"],
        "label": "Compare IA vs Architecture"
    }
]

def run_tests():
    print("Starting Logic Evaluation (Version 3 - Unicode Safe)...\n")
    success_count = 0
    
    for i, test in enumerate(test_cases):
        print(f"CASE {i+1}: {test['label']}")
        print(f"Q: {test['q']}")
        
        try:
            response = requests.post(BASE_URL, json={"message": test['q'], "session_id": f"eval_{i}"})
            if response.status_code == 200:
                answer = response.json().get('response', '')
                # Sanitise output for Windows terminal
                safe_answer = answer.encode('ascii', 'ignore').decode('ascii').lower()
                print(f"A: {safe_answer[:120]}...")
                
                # Check keywords in original lowercased answer
                lower_answer = answer.lower()
                matches = [kw for kw in test['must_contain'] if kw.lower() in lower_answer]
                
                if len(matches) >= 1: 
                    print("[OK] LOGICAL MATCH")
                    success_count += 1
                else:
                    print("[FAIL] ILLOGICAL OR WRONG RESP")
            else:
                print(f"[ERROR] SERVER ERROR: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] REQUEST FAILED: {str(e).encode('ascii', 'ignore').decode('ascii')}")
        
        print("-" * 30)
        time.sleep(1)

    accuracy = (success_count / len(test_cases)) * 100
    print(f"\nFINAL SCORE: {success_count}/{len(test_cases)} ({accuracy}%)")
    if accuracy >= 90:
        print("SUCCESS: Logic threshold met!")
    else:
        print("FAILURE: Logic needs more training.")

if __name__ == "__main__":
    run_tests()
