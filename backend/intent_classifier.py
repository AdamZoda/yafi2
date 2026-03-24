import sys
import os
import re
<<<<<<< HEAD

# Ensure the models are loaded once
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    
    # Load the same model used by FAISS to save memory and ensure compatibility
    # It's a small model so it should be fast
    intent_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
except ImportError:
    intent_model = None
=======
import numpy as np

# Ensure the models are loaded once
# Global cache for the embedding model to avoid reloading it
_shared_model = None

def get_shared_model(model_name='paraphrase-multilingual-MiniLM-L12-v2'):
    global _shared_model
    if _shared_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading shared embedding model: {model_name}...")
            _shared_model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
    return _shared_model

intent_model = get_shared_model()
>>>>>>> 3257fc1 (final)


class IntentClassifier:
    """
    A Zero-shot intent classifier that uses sentence embeddings.
    No ChatGPT required. It compares the user's message to a set of predefined 'anchor' sentences.
    Added hierarchical weighting combining embedding similarity + exact keyword boosts.
    """
    
    # Define intents and their anchor sentences (examples of what a user might say)
    INTENT_ANCHORS = {
        "CALCULATE_SCORE": [
            "Je veux calculer ma note",
            "Calcul de seuil",
            "J'ai eu 14 au régional et 15 au national",
            "Calcule moi mon score pour la médecine",
<<<<<<< HEAD
            "Quel est mon score avec ces notes ?"
=======
            "Quel est mon score avec ces notes ?",
            "Calculer mon score pour l'ENSA",
            "Puis-je faire médecine avec ma moyenne ?",
            "Seuils de présélection",
            "Estimation de mes chances d'admission"
>>>>>>> 3257fc1 (final)
        ],
        "COMPARE_SCHOOLS": [
            "Quelle est la différence entre ENSA et FST ?",
            "Compare l'ENCG et l'ISCAE",
            "Est-ce mieux médecine ou pharmacie ?",
            "Quels sont les avantages et inconvénients de l'UIR ?"
        ],
        "WHERE_TO_STUDY": [
            "Où puis-je étudier l'informatique ?",
            "Dans quelle ville y a-t-il une ENSA ?",
            "Quelles écoles y a-t-il à Casablanca ?",
            "Où faire de l'architecture ?",
            "Où se trouve l'ENSIAS ?",
            "Localisation de l'UIR"
        ],
        "SCHOLARSHIPS": [
            "Comment avoir une bourse de mérite ?",
            "Bourses disponibles UIR UM6P",
            "Quelles écoles offrent des bourses gratuites ?",
            "Dossier de bourse aide sociale",
            "Aide financière pour les études"
        ],
        "SCHOOL_FEES": [
            "Combien coûte l'inscription ?",
            "Quel est le prix de l'EMSI ?",
            "Frais de scolarité par an",
            "Tarifs des écoles privées de commerce",
            "Combien je dois payer ?"
        ],
        "ADMISSION_PROCEDURE": [
            "Comment s'inscrire à Minhaty ?",
            "Quelle est la procédure d'inscription ?",
            "Quels papiers pour le dossier ?",
            "Démarches pour s'inscrire en médecine",
            "Étapes pour postuler à une école"
        ],
        "FUTURE_JOBS": [
            "Quels sont les métiers d'avenir ?",
            "Métiers de demain",
            "Qu'est-ce que l'intelligence artificielle ?",
            "Emplois très demandés au Maroc",
            "Les métiers de l'IA"
        ],
        "GENERAL_ADVICE": [
            "Je suis perdu, que dois-je faire ?",
            "Que faire avec un bac PC ?",
            "Conseille-moi une stratégie",
            "Fais-moi un quiz d'orientation",
            "Bonjour, au revoir"
        ],
        "GENERAL_INFO": [
<<<<<<< HEAD
            "C'est quoi l'ENCG ?",
            "Définition de la FST",
            "Parle-moi de l'UM6P",
            "Qu'est-ce qu'un BTS ?",
            "Je veux des informations sur cette école"
=======
            "C'est quoi l'ENSA?", "Parle moi de l'UIR", "Infos sur l'EMSI", "Qu'est-ce que le DUT?", 
            "ESTS", "EMSI", "UIR", "UM6P", "ENSA", "ENCG", "FST", "EST", "ISCAE", "ENAM", "UIK"
        ],
        "FINANCIALS": [
            "Frais de scolarité", "Combien ça coûte ?", "Prix de l'école", "Budget annuel", "Frais d'inscription"
        ],
        "CAMPUS_LIFE": [
            "Est-ce qu'il y a un internat ?", "Les clubs étudiants", "Menu de la cantine", "Vie de campus", 
            "Dormir à l'école", "C'est quoi le menu de la cantine ?", "Y a-t-il un internat ?",
            "Quels sont les clubs et activités ?", "Comment est le campus ?", "Logement sur place"
>>>>>>> 3257fc1 (final)
        ],
        "RECOMMENDATION": [
            "Les meilleures écoles d'informatique",
            "Top des universités au Maroc",
            "Quelle est la meilleure option pour moi ?",
            "Classement des écoles d'ingénierie"
        ],
<<<<<<< HEAD
=======
        "SCHOOL_MAJORS": [
            "Quelles sont les filières de cette école ?",
            "Liste des spécialités à l'ENSA",
            "Qu'est-ce qu'on étudie à l'ESTS ?",
            "Quelles options pour le cycle ingénieur ?",
            "Est-ce qu'il y a du génie civil ici ?",
            "Filières disponibles",
            "Les branches d'études"
        ],
>>>>>>> 3257fc1 (final)
        "SOFT_SKILLS": [
            "Conseils pour gérer le stress",
            "Comment s'organiser pour le bac",
            "Méthode de révision",
            "Je stresse trop pour mes examens"
<<<<<<< HEAD
=======
        ],
        "SALARY_INFO": [
            "Quel est le salaire après l'EMSI ?",
            "Combien gagne un ingénieur ?",
            "Est-ce que l'informatique paye bien ?",
            "Salaire moyen à la sortie de l'école",
            "Quel est le taux d'insertion professionnelle ?"
>>>>>>> 3257fc1 (final)
        ]
    }

    # Keyword Weights for Hierarchical Scoring to resolve semantic overlap
    KEYWORD_WEIGHTS = {
        "COMPARE_SCHOOLS": [r"\bcompar(er|aison)\b", r"\bdifference\b", r"\bvs\b", r"\bentre\b"],
<<<<<<< HEAD
        "WHERE_TO_STUDY": [r"\boù\b", r"\bville\b", r"\blocalisation\b", r"\btrouve\b", r"\barchitecture\b", r"\betudi(er|ant)\b"],
        "SCHOLARSHIPS": [r"\bbourse\b", r"\bminhaty\b", r"\baide\b", r"\bgratuit(e|es)?\b", r"\bfinancement\b"],
        "SCHOOL_FEES": [r"\bprix\b", r"\bcout\b", r"\bfrais\b", r"\btarif\b", r"\bpay(er|ant|antes)?\b", r"\bcheres?\b", r"\bcombien\b", r"\bmoins\s+cheres?\b"],
        "ADMISSION_PROCEDURE": [r"\bprocedure\b", r"\binscription(s)?\b", r"\bdossier\b", r"\betape(s)?\b", r"\bpostuler\b", r"\bcomment\b", r"\bconcours\b", r"\bquand\b"],
        "FUTURE_JOBS": [r"\bavenir\b", r"\bmetier(s)?\b", r"\bemploi(s)?\b", r"\btravail\b", r"\bsalaire\b", r"\b(ia|ai)\b", r"\bintelligence\b", r"\bdebou(che|ches)\b", r"\bremplacer\b"],
        "CALCULATE_SCORE": [r"\bcalcul(er)?\b", r"\bnote\b", r"\bscore\b", r"\bseuil\b", r"\bmoyenne\b"],
        "GENERAL_INFO": [r"\bc'est quoi\b", r"\b(definition|definition)\b", r"\bqu'est-ce\b"],
        "RECOMMENDATION": [r"\bmeilleur(e|s|es)?\b", r"\btop\b", r"\bclassement\b", r"\bbien\b"],
        "SOFT_SKILLS": [r"\bstress\b", r"\borganisation\b", r"\brevision(s)?\b", r"\bsommeil\b"],
        "GENERAL_ADVICE": [r"\bbonjour\b", r"\bsalut\b", r"\bcherche\b", r"\baide\b"]
=======
        "WHERE_TO_STUDY": [r"\boù\b", r"\bville\b", r"\blocalisation\b", r"\btrouve\b", r"\barchitecture\b", r"\betudi(er|ant)\b", r"\b(casablanca|rabat|marrakech|tanger|agadir|fes|fès|meknes|meknès|tetouan|settat|el jadida|beni mellal|safi|nador|oujda|kenitra|khouribga|berrechid|taza|errachidia|al hoceima|ifrane|benguerir)\b"],
        "SCHOLARSHIPS": [r"\bbourse(s)?\b", r"\bminhaty\b", r"\baide\b", r"\bgratuit(e|es)?\b", r"\bfinancement\b"],
        "SCHOOL_FEES": [r"\bprix\b", r"\bcout\b", r"\bfrais\b", r"\btarif\b", r"\bpay(er|ant|antes)?\b", r"\bcher(e|es|s)?\b", r"\bcombien\b", r"\bmoins\s+cher(e|es|s)?\b"],
        "ADMISSION_PROCEDURE": [r"\bprocedure\b", r"\binscription(s)?\b", r"\bdossier\b", r"\betape(s)?\b", r"\bpostuler\b", r"\bcomment\s+(m'inscrire|s'inscrire|postuler|acceder|integrer)\b", r"\bconcours\b", r"\bquand\b"],
        "FUTURE_JOBS": [r"\bavenir\b", r"\bmetier(s)?\b", r"\bemploi(s)?\b", r"\btravail\b", r"\bsalaire\b", r"\b(ia|ai)\b", r"\bintelligence\b", r"\bdebou(che|ches)\b", r"\bremplacer\b", r"\bdevenir\b", r"\bingenieur\b"],
        "CALCULATE_SCORE": [r"\bcalcul(er)?\b", r"\bnote\b", r"\bscore\b", r"\bseuil\b", r"\bmoyenne\b", r"\b1[0-9](\.[0-9]+)?\b"],
        "GENERAL_INFO": [r"\bc'est quoi\b", r"\bdefinition\b", r"\bqu'est-ce\b"],
        "RECOMMENDATION": [r"\bmeilleur(e|s|es)?\b", r"\btop\b", r"\bclassement\b", r"\bbien\b"],
        "SOFT_SKILLS": [r"\bstress\b", r"\borganisation\b", r"\brevision(s)?\b", r"\bsommeil\b"],
        "GENERAL_ADVICE": [r"\bbonjour\b", r"\bsalut\b", r"\bcherche\b", r"\baide\b"],
        "SALARY_INFO": [r"\bsalaire\b", r"\bgagne(r)?\b", r"\bisertion\b", r"\bpaye\b", r"\bremune(ration)?\b", r"\bembauche\b"],
        "CAMPUS_LIFE": [r"\bmenu\b", r"\bcantine\b", r"\bmanger\b", r"\brepas\b", r"\bclub(s)?\b", r"\bevent(s)?\b", r"\bsport\b", r"\baccessible\b", r"\btransport\b", r"\binternat\b", r"\blogement\b", r"\bdortoir(s)?\b", r"\bresidence(s)?\b"],
        "SCHOOL_MAJORS": [r"\bfiliere(s)?\b", r"\bspecialite(s)?\b", r"\bbranche(s)?\b", r"\boption(s)?\b"]
>>>>>>> 3257fc1 (final)
    }

    def __init__(self):
        if not intent_model:
<<<<<<< HEAD
            print("⚠️ IntentClassifier: sentence-transformers not installed. Intent classification disabled.")
=======
            print("IntentClassifier: sentence-transformers not installed. Intent classification disabled.")
>>>>>>> 3257fc1 (final)
            self.enabled = False
            return
            
        self.enabled = True
        self.intent_embeddings = {}
        
        # Precompute embeddings for all anchors for fast comparison
<<<<<<< HEAD
        print("💡 Pre-computing intent embeddings...")
=======
        print("Pre-computing intent embeddings...")
>>>>>>> 3257fc1 (final)
        for intent, anchors in self.INTENT_ANCHORS.items():
            self.intent_embeddings[intent] = intent_model.encode(anchors)
            
    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def classify(self, user_message: str, threshold: float = 0.5):
        """
        Classifies the user message into one of the predefined intents.
        Uses a hierarchical score: Embedding Similarity + Keyword Matches.
        Returns the intent name, or None if the confidence is too low.
        """
        if not self.enabled or len(user_message.strip()) < 5:
            return None
            
        msg_emb = intent_model.encode(user_message)
        
        best_intent = None
        best_score = -1
        
        # 1. Semantic Score
        semantic_scores = {}
        for intent, anchors_emb in self.intent_embeddings.items():
            scores = [self.cosine_similarity(msg_emb, a_emb) for a_emb in anchors_emb]
            semantic_scores[intent] = max(scores)
            
        # 2. Hierarchical Score = Semantic Score + Keyword Boost
        final_scores = {}
        user_message_lower = user_message.lower()
        
        # Safety Lock: if we find highly specific conflicting words, we drop competing intents
        is_architecture = re.search(r'\barchitecture\b', user_message_lower)
        
        for intent, score in semantic_scores.items():
            bonus = 0.0
            
            # Penalize conflicting overlaps
            if is_architecture and intent == "FUTURE_JOBS":
                bonus -= 0.8 # Very strong penalty to override semantic similarity
                
            if intent in self.KEYWORD_WEIGHTS:
                for pattern in self.KEYWORD_WEIGHTS[intent]:
                    if re.search(pattern, user_message_lower, re.IGNORECASE):
<<<<<<< HEAD
                        bonus += 0.4 # Overwhelming boost to ensure explicit keywords win
=======
                        bonus += 0.8 # Overwhelming boost to ensure explicit keywords win
>>>>>>> 3257fc1 (final)
            
            final_scores[intent] = score + bonus
            
            if final_scores[intent] > best_score:
                best_score = final_scores[intent]
                best_intent = intent
                
        if best_score >= threshold:
<<<<<<< HEAD
            print(f"🎯 INTENT DETECTED: {best_intent} (Score: {best_score:.2f}, Semantic: {semantic_scores[best_intent]:.2f})")
            return best_intent
        
        print(f"🤷 INTENT UNCERTAIN (Best was {best_intent} with {best_score:.2f})")
=======
            print(f"INTENT DETECTED: {best_intent} (Score: {best_score:.2f}, Semantic: {semantic_scores[best_intent]:.2f})")
            return best_intent
        
        print(f"INTENT UNCERTAIN (Best was {best_intent} with {best_score:.2f})")
>>>>>>> 3257fc1 (final)
        return None

    def extract_entities(self, text: str) -> dict:
        """
        Extracts key entities (Bac, Moyenne, Budget, Ville, Ecole) using regex.
        Matches the parameters needed for Prolog calculations.
        """
        text_lower = text.lower()
        entities = {
            "bac": None,
            "moyenne": None,
            "budget": None,
            "ville": None,
            "ecole": None
        }

        # 1. Bac Type
        bac_patterns = {
            "PC": r"\b(pc|physique|chimie)\b",
            "SVT": r"\b(svt|sciences\s+vie|biologie)\b",
            "SM": r"\b(sm|sciences\s+maths?)\b",
            "ECO": r"\b(eco|economie|gestion)\b",
            "PRO": r"\b(pro|professionnel)\b"
        }
        for code, pattern in bac_patterns.items():
            if re.search(pattern, text_lower):
                entities["bac"] = code
                break

        # 2. Moyenne (Search for numbers around 10-20)
        moyenne_match = re.search(r"\b(1\d(\.\d{1,2})?|20|10)\b", text)
        if moyenne_match:
            entities["moyenne"] = float(moyenne_match.group(1))

        # 3. Budget (Search for larger numbers or keywords)
        budget_match = re.search(r"\b(\d{4,6})\b", text)
        if budget_match:
            entities["budget"] = int(budget_match.group(1))

        # 4. Schools (Main Sigles)
<<<<<<< HEAD
        school_patterns = ["ENSA", "ENCG", "FST", "FMP", "EST", "UM6P", "UIR", "ISCAE", "ENA"]
=======
        # Avoid matching 'est' (verb) for 'EST' (school) unless it's likely a school context
        school_patterns = [
            "ENSA", "ENCG", "FST", "FMP", "UM6P", "UIR", "ISCAE", "ENA", 
            "EMSI", "ENSAM", "ENSIAS", "IAV", "ISIC", "INAU", "ISADAC", "ESBA", "INBA"
        ]
        
        # Check specific schools first
>>>>>>> 3257fc1 (final)
        for school in school_patterns:
            if re.search(r"\b" + re.escape(school) + r"\b", text, re.IGNORECASE):
                entities["ecole"] = school
                break
<<<<<<< HEAD
=======
        
        # Special case for EST to avoid 'c'est' or 'est' verb match
        if not entities["ecole"]:
            if re.search(r"\bEST\b", text) or (re.search(r"\b(à|et|école)\s+est\b", text_lower)):
                entities["ecole"] = "EST"
>>>>>>> 3257fc1 (final)

        # 5. Cities
        cities = ["Casablanca", "Rabat", "Marrakech", "Agadir", "Fes", "Tanger", "Oujda", "Meknes", "Safi"]
        for city in cities:
            if re.search(r"\b" + re.escape(city) + r"\b", text, re.IGNORECASE):
                entities["ville"] = city
                break

        return entities
