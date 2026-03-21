import json
import requests
import time

# -------------------------------------------------------------
# 1. THE MASSIVE 33 QUESTION TEST SUITE (UI Suggestions + Evil Cases)
# -------------------------------------------------------------

test_cases = [
    # --- PART 1: UI SUGGESTIONS (Immediate impact) ---
    {
        "q": "J'ai une moyenne de 12, que faire ?",
        "must_contain": ["sciences", "universit", "technique", "conseil", "12"],
        "label": "UI: Low Grade Advice"
    },
    {
        "q": "Quels sont les débouchés pour un Bac SVT ?",
        "must_contain": ["medecine", "fmp", "paramedical", "ispits", "svt"],
        "label": "UI: SVT Paths"
    },
    {
        "q": "C'est quoi l'ENCG ?",
        "must_contain": ["commerce", "gestion", "reseau", "ecole", "encg"],
        "label": "UI: Definition ENCG (GENERAL_INFO)"
    },
    {
        "q": "Comment s'inscrire à la Fac ?",
        "must_contain": ["universite", "fac", "inscription", "dossier", "etape"],
        "label": "UI: Fac Procedure"
    },
    {
        "q": "Y a-t-il une ENSA à Tanger ?",
        "must_contain": ["oui", "ensa", "tanger"],
        "label": "UI: Location Specificity"
    },
    {
        "q": "Quel était le seuil de médecine 2023 ?",
        "must_contain": ["13", "14", "seuil", "medecine", "2023"],
        "label": "UI: Historical Threshold"
    },
    {
        "q": "Différence entre FST et Fac ?",
        "must_contain": ["compar", "differen", "fst", "fac", "technique", "universite"],
        "label": "UI: FST vs Fac Comparison"
    },
    {
        "q": "Comment avoir une bourse Minhaty ?",
        "must_contain": ["minhaty", "bourse", "massar", "revenu", "portail"],
        "label": "UI: Minhaty Procedure"
    },
    {
        "q": "Quels sont les frais de l'UIR ?",
        "must_contain": ["72", "90", "dh", "uir"],
        "label": "UI: UIR Fees"
    },
    {
        "q": "Est-ce que je peux faire ingénieur avec un Bac Eco ?",
        "must_contain": ["non", "impossible", "eco", "ingenieur", "scientifique"],
        "label": "UI: Eco to Engineering (Logic Block)"
    },
    {
        "q": "Où étudier l'architecture au Maroc ?",
        "must_contain": ["ena", "uir", "architecture", "ecole"],
        "label": "UI: Architecture locations"
    },
    {
        "q": "Conseils pour gérer le stress du Bac",
        "must_contain": ["stress", "gestion", "respir", "sommeil", "organisation"],
        "label": "UI: Soft Skills QA"
    },
    {
        "q": "Les meilleures écoles d'informatique ?",
        "must_contain": ["ensias", "ensa", "inpt", "emsi", "meilleur"],
        "label": "UI: Recommendations"
    },
    
    # --- PART 2: THE 20 EVIL EDGE CASES (Human-Like Chaos) ---
    {
        "q": "Je veux devenir medcin mais j'ai que 10 de moyenne bac pc",
        "must_contain": ["difficile", "seuil", "10", "prive", "etranger", "medecine"],
        "label": "EVIL 1: Bad Grade Reality Check"
    },
    {
        "q": "Et pour la pharmacie ?", # Context follow up test
        "must_contain": ["pharmacie", "seuil", "fmp"],
        "label": "EVIL 2: Context Carry (Needs to remember EVIL 1 context)"
    },
    {
        "q": "c koi l'um6ppp ?", # Extreme typol
        "must_contain": ["um6p", "benguerir", "polytechnique", "excellence"],
        "label": "EVIL 3: Extreme fuzzy NER & Definition"
    },
    {
        "q": "Le prix de l'ensa",
        "must_contain": ["gratuit", "public", "0 dh", "ensa"],
        "label": "EVIL 4: Fees of a Public School"
    },
    {
        "q": "Je veux étudier à l'étranger (France)",
        "must_contain": ["campus", "france", "etranger", "tcf", "visa"],
        "label": "EVIL 5: Out of scope but handled gracefully"
    },
    {
        "q": "Quelles sont les ecoles payantes à Rabat pour faire de l'informatique ?",
        "must_contain": ["uir", "emsi", "rabat", "informatique", "payant"],
        "label": "EVIL 6: Multi-constraint query (City, Type, Domain)"
    },
    {
        "q": "Est ce que je dois passer un concours pour l'OFPPT ?",
        "must_contain": ["non", "direct", "dossier", "ofppt"],
        "label": "EVIL 7: Procedure Specificity (No exam)"
    },
    {
        "q": "Compare la durée des études entre médecine et ingénierie",
        "must_contain": ["7", "5", "ans", "medecine", "ingenierie", "compar"],
        "label": "EVIL 8: Duration Comparison"
    },
    {
        "q": "Si je fais l'ENGC et apres je veux changer vers medecine ?",
        "must_contain": ["impossible", "passerelle", "bac", "scientifique"],
        "label": "EVIL 9: Complex pathway change"
    },
    {
        "q": "cb ca coute", # "Combien ça coûte" (extreme slang)
        "must_contain": ["quoi", "ecole", "precisez"],
        "label": "EVIL 10: Slang + Missing Entity Fallback"
    },
    {
        "q": "emsi", # Just the entity
        "must_contain": ["emsi", "que veux-tu", "prix", "procedure"],
        "label": "EVIL 11: Just Entity (Prompt for attribute)"
    },
    {
        "q": "Est ce que l'IA va remplacer les ingenieurs ?",
        "must_contain": ["futur", "avenir", "metier", "remplacer", "ia"],
        "label": "EVIL 12: Existential Job Question"
    },
    {
        "q": "Donne moi les ecoles privées les moins chères",
        "must_contain": ["moins cher", "emsi", "ehec", "prix"],
        "label": "EVIL 13: Qualitative Pricing"
    },
    {
        "q": "Je suis nul en maths, je fais quoi ?",
        "must_contain": ["lettres", "arts", "droit", "commerce", "maths"],
        "label": "EVIL 14: Skill based routing"
    },
    {
        "q": "L'ENCG c'est bien ?",
        "must_contain": ["oui", "excellence", "commerce", "reseau", "encg"],
        "label": "EVIL 15: Vague opinion request"
    },
    {
        "q": "Bourse pour l'UIR si j'ai 13 de moyenne",
        "must_contain": ["partielle", "social", "14", "16", "uir"],
        "label": "EVIL 16: Conditional scholarship"
    },
    {
        "q": "Quels metiers rapporte le plus dargent au maroc",
        "must_contain": ["salaire", "ia", "medecine", "finance", "argent"],
        "label": "EVIL 17: Salary focus"
    },
    {
        "q": "Je déteste l'informatique",
        "must_contain": ["eviter", "commerce", "sante", "droit", "informatique"],
        "label": "EVIL 18: Negative constraint"
    },
    {
        "q": "Quand commencent les inscriptions pour minhaty",
        "must_contain": ["date", "juin", "periode", "minhaty"],
        "label": "EVIL 19: Time/Date extraction"
    },
    {
        "q": "Bonjour, je cherche une école.",
        "must_contain": ["bonjour", "profil", "bac", "quel", "orienter"],
        "label": "EVIL 20: Greetings into routing"
    }
]

import unicodedata

def normalize_text(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', str(text)) if unicodedata.category(c) != 'Mn')
    return text.lower()

session_id = f"eval_huge_{int(time.time())}"
score = 0
total = len(test_cases)

print("--- STARTING MASSIVE 33-QUESTION HUMAN-LIKE EVALUATION")
print("============================================================\n")

logfile = open("results.log", "w", encoding="utf-8")

def safe_print(text):
    try:
        logfile.write(text + "\n")
    except:
        pass

for i, test in enumerate(test_cases, 1):
    q = test["q"]
    expected_words = test["must_contain"]
    label = test["label"]
    
    safe_print(f"[{i}/{total}] {label}")
    safe_print(f"Q: {q}")
    
    try:
        # Keep same session_id to test context carryover
        res = requests.post('http://127.0.0.1:5000/chat', json={'message': q, 'session_id': session_id}).json()
        response_text = res.get('response', '')
        
        reply_norm = normalize_text(response_text)
        
        # Check if AT LEAST ONE of the must_contain words is present
        matched_words = [word.lower() for word in expected_words if normalize_text(word).lower() in reply_norm]
        
        if len(matched_words) >= min(2, len(expected_words)):
            safe_print("[PASS]")
            score += 1
        else:
            safe_print("[FAIL]")
            safe_print(f"Missing keywords. Expected at least 2 from: {expected_words}")
            safe_print(f"Matched only: {matched_words}")
            safe_print(f"A: {response_text[:150]}...")
            
    except Exception as e:
        safe_print(f"[ERROR] {e}")
        
    safe_print("-" * 50)

safe_print(f"\n--- FINAL SCORE: {score}/{total} ({round(score/total*100, 2)}%)")
if score < total * 0.90:
    safe_print("--- NEEDS MORE TRAINING")
else:
    safe_print("--- SUCCESS! MODEL IS HUMAN-LIKE")
logfile.close()

