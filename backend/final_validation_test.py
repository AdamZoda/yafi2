
import requests
import json
import time

BASE_URL = "http://localhost:5000/chat"

questions = [
    # --- Logique et Recommandation ---
    "J'ai un Bac SVT avec 14.5 de moyenne, est-ce que je peux faire médecine selon tes règles ?",
    "Quelle est la stratégie conseillée pour un élève qui a 12.5 de moyenne au Bac ?",
    "Je suis en Bac PC, quelles sont les filières 'Idéales' pour mon profil ?",
    "Est-ce qu'un Bac Éco peut faire une école d'ingénierie publique ?",
    "Quelle est la différence de conseil entre un profil avec 16 de moyenne et un profil avec 10 ?",
    "Recommande-moi une orientation pour un Bac SM intéressé par l'Informatique & Data.",
    "Un Bac Lettres peut-il faire de l'informatique selon ta base ?",
    "Quels sont les avantages et les limites d'un Bac PC ?",
    "Quelles sont les filières recommandées pour un Bac Éco ?",
    "J'ai un Bac SVT, est-ce que l'ingénierie est 'Possible' ou 'Excellente' pour moi ?",

    # --- Données Factuelles ---
    "Où se trouve l'UM6P ?",
    "Donne-moi la liste des villes où on trouve une ENSA.",
    "Quelles sont les écoles situées à Benguerir ?",
    "Est-ce qu'il y a une EST à Safi ?",
    "Quelles sont les villes considérées comme des villes 'Opportunité' ?",
    "Cite-moi trois villes à forte concurrence pour les études.",
    "L'ENSAM est-elle présente à Casablanca ?",
    "Où peut-on étudier le management hôtelier en privé ?",
    "Quelles sont les écoles d'ingénierie présentes à Rabat ?",
    "Dans quelle ville se trouve l'Université Al Akhawayn ?",

    # --- Détails, Frais et Procédures ---
    "Combien coûtent les frais de scolarité à l'EMSI ?",
    "Quelle est la définition du système LMD ?",
    "Quel est le seuil de l'ENSA en 2023 ?",
    "Quelles sont les spécialités proposées par l'UIR ?",
    "Quels sont les 'Pros' et 'Cons' d'une école privée ?",
    "Quelle est la différence entre un BTS et un DUT selon tes définitions ?",
    "Comment se déroule le concours de médecine (épreuves et coefficients) ?",
    "Quel est le salaire moyen d'un ingénieur débutant au Maroc ?",
    "Quels sont les documents ou procédures pour le dossier Minhaty ?",
    "Quelle est la plateforme pour s'inscrire aux écoles publiques ?"
]

def run_test():
    session_id = f"test_final_{int(time.time())}"
    results = []

    for i, q in enumerate(questions, 1):
        session_id = f"test_final_{i}_{int(time.time())}" # Unique session per question
        print(f"Running Q{i}: {q}")
        payload = {
            "message": q,
            "session_id": session_id,
            "stream": False
        }
        try:
            response = requests.post(BASE_URL, json=payload, timeout=60) # Increased timeout to 60s
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "id": i,
                    "question": q,
                    "response": data.get("response", "ERROR: No response"),
                    "source": data.get("source", "unknown"),
                    "entities": data.get("entities", {})
                })
            else:
                results.append({"id": i, "question": q, "response": f"ERROR: Status {response.status_code}"})
        except Exception as e:
            results.append({"id": i, "question": q, "response": f"EXCEPTION: {str(e)}"})
        
        time.sleep(1) # Small delay to avoid overloading local ollama

    with open("c:/Users/PC/Downloads/YAFI/yafi2-main/backend/final_validation_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("\nTest Complete. Results saved to final_validation_results.json")

if __name__ == "__main__":
    run_test()
