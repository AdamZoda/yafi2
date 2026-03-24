import requests
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
    with open("eval_results_utf8.txt", "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("🚀 EVALUATION DES 31 SUGGESTIONS\n")
        f.write("="*60 + "\n")
        
        for i, q in enumerate(SUGGESTIONS, 1):
            f.write(f"\n[{i}/31] QUESTION : {q}\n")
            try:
                res = requests.post("http://localhost:5000/chat", json={
                    "message": q,
                    "session_id": "eval_test_final",
                    "stream": False
                }, timeout=30)
                data = res.json()
                source = data.get("source", "UNKNOWN")
                text = data.get("response", "")
                
                status = "✅ SUCCES"
                cause = ""
                lower_text = text.lower()
                if len(text) < 20 or "je n'ai pas" in lower_text or "pas d'information" in lower_text or "erreur" in lower_text or "précisez" in lower_text:
                    status = "❌ ECHEC / INFO MANQUANTE"
                    if source == "prolog_expert":
                        cause = "(Info absente de la base Prolog, ou entité non détectée)"
                    else:
                        cause = "(RAG n'a pas trouvé l'info dans les textes vectoriels)"
                
                f.write(f"  SOURCE : {source}\n")
                f.write(f"  REPONSE: {text[:200].replace(chr(10), ' ')}...\n")
                f.write(f"  STATUT : {status} {cause}\n")
                
            except Exception as e:
                f.write(f"  ❌ ERREUR DE REQUETE : {e}\n")
            time.sleep(0.5)

if __name__ == '__main__':
    evaluate()
