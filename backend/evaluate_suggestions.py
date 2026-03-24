import requests
import json
import time

SUGGESTIONS = [
    "Comparer EMSI et UIR (Salaires & Débouchés)",
    "Écoles d'ingénierie budget < 45000 DH",
    "Quel est le salaire moyen après l'EMSI ?",
    "Menu de la cantine à l'UIK aujourd'hui",
    "Calendrier des concours 2026 au Maroc",
    "Meilleure école d'info avec un Bac PC",
    "Différence entre ENSA et ENAM ?",
    "Bourses d'excellence à l'UM6P",
    "Frais de scolarité de l'ISCAE",
    "Est-ce que l'UIR a un internat ?",
    "Métiers d'avenir dans l'IA au Maroc",
    "Comment s'inscrire sur CursusSup ?",
    "Seuils médecine 2025 (Estimations)",
    "Filières possibles avec un Bac SM",
    "Calculer mon score pour l'ENSA",
    "Quiz : Quelle école me correspond ?",
    "Conseils pour réussir le concours ENCG",
    "Liste des écoles d'architecture privées",
    "Différence entre Licence Pro et Fondamentale",
    "Débouchés après un Bac Eco-Gestion",
    "Comment avoir la bourse Minhaty ?",
    "Écoles avec prépa intégrée à Casablanca",
    "Avantages du système LMD au Maroc",
    "Puis-je faire médecine avec 14 de moyenne ?",
    "Le diplôme de l'OFPPT est-il reconnu ?",
    "Meilleure méthode pour réviser le Bac",
    "Vaut-il mieux faire un BTS ou un DUT ?",
    "Frais d'inscription à l'Université Privée de Fès",
    "Comment devenir ingénieur en cybersécurité ?",
    "Les clubs étudiants à l'EMSI",
    "Prochaines dates d'inscription OFPPT"
]

def evaluate():
    print("="*60)
    print("🚀 DÉMARRAGE DE L'ÉVALUATION DES 31 SUGGESTIONS")
    print("="*60)
    
    for i, q in enumerate(SUGGESTIONS, 1):
        print(f"\n[{i}/31] QUESTION : {q}")
        try:
            res = requests.post("http://localhost:5000/chat", json={
                "message": q,
                "session_id": "eval_test",
                "stream": False
            }, timeout=30)
            data = res.json()
            source = data.get("source", "UNKNOWN")
            text = data.get("response", "")
            
            # Simple heuristic for evaluation
            status = "✅ SUCCÈS"
            cause = ""
            lower_text = text.lower()
            if len(text) < 20 or "je n'ai pas" in lower_text or "pas d'information" in lower_text or "erreur" in lower_text or "précisez" in lower_text:
                status = "❌ ÉCHEC / INFO MANQUANTE"
                if source == "prolog_expert":
                    cause = "(Info absente de la base Prolog, ou entité non détectée)"
                else:
                    cause = "(RAG n'a pas trouvé l'info dans les textes vectoriels)"
            
            print(f"  SOURCE : {source}")
            print(f"  RÉPONSE: {text[:100].replace(chr(10), ' ')}...")
            print(f"  STATUT : {status} {cause}")
            
        except Exception as e:
            print(f"  ❌ ERREUR DE REQUÊTE : {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    evaluate()
