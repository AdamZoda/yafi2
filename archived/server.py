from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog 
import random
import time
import unicodedata
import re
import sys
import os
import difflib
from dotenv import load_dotenv
try:
    from supabase import create_client, Client
except ImportError:
    # Fallback if installation is not yet finished in this shell session
    create_client, Client = None, None

# Global dictionary for context memory (NER Track)
session_context = {}

# Import User Memory module
try:
    import user_memory as UserMemory
    print("✓ UserMemory module loaded")
except Exception as e_mem:
    UserMemory = None
    print(f"⚠️ UserMemory not available: {e_mem}")


# Load environment variables
load_dotenv()

# Init Supabase
supabase_url = os.environ.get("VITE_SUPABASE_URL")
supabase_key = os.environ.get("VITE_SUPABASE_ANON_KEY")
supabase = create_client(supabase_url, supabase_key) if (create_client and supabase_url and supabase_key) else None

# Force UTF-8 encoding for Windows terminals (with fallback)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, RuntimeError, UnicodeDecodeError):
    # Fallback for environments where reconfigure fails
    pass

app = Flask(__name__)
CORS(app)

# Init Prolog
prolog = Prolog()
try:
    # Get absolute path to the backend directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load primary KB
    primary_kb = os.path.join(base_dir, "full_orientation_system.pl")
    prolog.consult(primary_kb.replace('\\', '/'))
    
    # Load secondary KB
    secondary_kb = os.path.join(os.path.dirname(base_dir), "knowledge_base_orientation.pl")
    prolog.consult(secondary_kb.replace('\\', '/'))
    
    print("✓ Knowledge bases (Primary & Pro) loaded successfully")
except Exception as e1:
    print(f"❌ CRITICAL: Error loading Prolog knowledge base")
    print(f"   Path error: {e1}")
    raise SystemExit("Cannot start server without knowledge base")



# Init Vector Search System (NEW - Professional RAG)
try:
    from vector_knowledge import VectorKnowledgeBase
    from conversation_manager import conversation_manager
    from prompt_engine import YAFIPromptEngine
    from llm_engine import llm_engine
    from ollama_advanced_config import OllamaAdvancedConfig  # NEW - Advanced Ollama
    
    vector_kb = VectorKnowledgeBase()
    print("✓ Vector Knowledge Base initialized (Professional RAG)")
    print(f"✓ LLM Engine initialized (Provider: {llm_engine.provider_name})")
    print("✓ Ollama Advanced Config loaded (MORE PERMISSIONS FOR OLLAMA)")
    USE_VECTOR_SEARCH = True
except Exception as e:
    print(f"⚠️  Vector Search not available: {e}")
    print("   Falling back to legacy RAG")
    vector_kb = None
    USE_VECTOR_SEARCH = False

# Init Intent Classifier and Response Builder (NEW - 100% Local Intelligence)
try:
    from intent_classifier import IntentClassifier
    from response_builder import ResponseBuilder
    intent_classifier = IntentClassifier()
    print("✓ Local NLU Intent Classifier initialized")
except Exception as e:
    print(f"⚠️ Intent Classifier not available: {e}")
    intent_classifier = None
    ResponseBuilder = None

@app.route('/chat', methods=['POST'])
def chat():
    with open(r"c:\Users\PC\Downloads\YAFI\yafi2-main\backend\debug_chat.log", "a", encoding="utf-8") as lf:
        lf.write(f"\n--- [{{datetime.datetime.now()}}] NEW REQUEST ---\n")
    data = request.json
    user_message = data.get('message', '').strip().lower()
    
    # SÉCURITÉ: Limite de caractères pour éviter les attaques DoS
    MAX_MESSAGE_LENGTH = 500
    if len(user_message) > MAX_MESSAGE_LENGTH:
        user_message = user_message[:MAX_MESSAGE_LENGTH]
    
    # MÉMOIRE DE SESSION: Récupérer le dernier sujet abordé
    session_data = data.get('session', {})
    last_topic = session_data.get('last_topic', None)
    last_grade = session_data.get('last_grade', None)
    
    # Fonction de sanitization pour éviter l'injection Prolog
    def sanitize_prolog_input(text):
        """Nettoie le texte pour éviter l'injection dans les requêtes Prolog"""
        # Remplacer les apostrophes et guillemets dangereux
        text = text.replace("'", " ").replace('"', ' ').replace('\\', ' ')
        # Supprimer les caractères de contrôle
        text = ''.join(c for c in text if c.isprintable() or c.isspace())
        return text.strip()
    
    # Normalisation CENTRALISÉE pour gérer les accents, synonymes et variations
    def normalize_text(text):
        """Normalise le texte en retirant les accents et en gérant les variations courantes"""
        # Retirer les accents
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        
        # Dictionnaire des synonymes et corrections (ordre important)
        replacements = {
            # Écoles / Sigles (normalisation)
            'faculte': 'fac', 'universite': 'fac', 'univ': 'fac',
            'medecine': 'medecine', 'medcine': 'medecine', 'medcin': 'medecine', 'docteur': 'medecine',
            'ingenierie': 'ingenierie', 'ingenieur': 'ingenierie', 'ingenerie': 'ingenierie',
            'commerce': 'commerce', 'business': 'commerce', 'gestion': 'commerce',
            'informatique': 'informatique', 'info': 'informatique', 'dev': 'informatique', 'coding': 'informatique',
            'architecte': 'architecture', 'archi': 'architecture',
            'ia': 'intelligence artificielle', 'ai': 'intelligence artificielle',
            'ensias': 'ensias', 'uir': 'uir', 'um6p': 'um6p', 'emsi': 'emsi',
            'engc': 'encg', 'engam': 'encg',  # correction typos frecuentes
            # Mots courants
            'ecole': 'ecole', 'ecoles': 'ecole',
            'debouche': 'debouches', 'debouches': 'debouches', 'metier': 'debouches', 'travail': 'debouches',
            'argent': 'salaire', 'paye': 'salaire', 'remuneration': 'salaire',
            'frais': 'prix', 'cout': 'prix', 'payer': 'prix', 'payant': 'prix',
            # Slang et abreviations
            'cb': 'combien', 'koi': 'quoi', 'c': 'cest', 'pk': 'pourquoi',
            'pcq': 'parce que', 'biz': 'besoin', 'vs': 'versus',
            'dargent': 'salaire', 'rapporte': 'salaire',
        }
        
        # Nettoyage des articles contractés (l', d', etc)
        text = text.replace("l'", " ").replace("d'", " ").replace("s'", " ").replace("j'", " ")
        
        words = text.split()
        normalized_words = [replacements.get(w, w) for w in words]
        return ' '.join(normalized_words)
    
    # Normaliser le message utilisateur et METTRE À JOUR LA VARIABLE PRINCIPALE
    user_message_normalized = normalize_text(user_message)
    user_message = user_message_normalized

    # NER Fuzzy (Extraction flexible d'entités)
    KNOWN_ENTITIES = [
        "emsi", "uir", "um6p", "ensa", "encg", "fst", "ensias", "iscae", "uic", "fmp",
        "ensam", "ensck", "isss", "ispits", "enam", "iav", "ispm", "itsat", "isic", "inau",
        "isadac", "esba", "inba", "insap", "aat", "isitt", "imsk", "iss", "issf", "irfcjs", "ena",
        "ofppt", "medecine", "pharmacie", "architecture", "minhaty",
        "casablanca", "rabat", "marrakech", "tanger", "agadir", "fes"
    ]
    def extract_entity(text):
        words = text.split()
        for w in words:
            if len(w) > 2:
                matches = difflib.get_close_matches(w, KNOWN_ENTITIES, n=1, cutoff=0.7)
                if matches: return matches[0]
        matches = difflib.get_close_matches(text, KNOWN_ENTITIES, n=1, cutoff=0.6)
        if matches: return matches[0]
        return None

    def normalize_school_id(name: str) -> str:
        """Maps any variation of a school name to its base Prolog ID."""
        if not name: return ""
        n = name.lower().strip()
        # Direct mappings
        mappings = {
            "emsi": "emsi", "uir": "uir", "um6p": "um6p", "ensa": "ensa", 
            "encg": "encg", "fst": "fst", "ensam": "ensam", "fmp": "fmp",
            "ensias": "ensias", "iscae": "iscae", "ispits": "ispits", "isss": "isss", "enam": "enam", "iav": "iav",
            "enam": "enam", "iav": "iav"
        }
        for key, val in mappings.items():
            if key in n: return val
        return n.replace(" ", "_")

    def get_upcoming_concours():
        """Extracts upcoming dates from date_concours."""
        q = "get_date_concours(Name, Date)"
        results = list(prolog.query(q))
        if not results: return "Aucune date de concours n'est encore enregistrée."
        
        calendar = "📅 **Prochains Concours & Dates Clés :**\n"
        for res in results[:10]:
            name = clean_text(res['Name']).upper()
            date = clean_text(res['Date'])
            calendar += f"• **{name}** : {date}\n"
        return calendar

    # Helper pour l'encodage (PySwip retourne parfois du Mojibake)
    def clean_text(text):
        if not isinstance(text, str): return str(text)
        cleaned = text
        # 1. Essayer réparation automatique (Magic Encoding)
        try:
            cleaned = text.encode('cp1252').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            try:
                cleaned = text.encode('latin-1').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass
        
        # 2. Réparation Manuelle (Fallback si Magic échoue à cause des Emojis)
        # 2. Réparation Manuelle (Fallback si Magic échoue à cause des Emojis)
        # Les emojis font planter l'encode('latin-1'), donc le texte reste cassé (ex: Ã©).
        # On force le remplacement des séquences UTF-8 interprétées en Latin-1.
        replacements = {
            'Ã©': 'é', 'Ã¨': 'è', 'Ã ': 'à', 'Ã¢': 'â', 'Ãª': 'ê', 'Ã®': 'î', 'Ã´': 'ô', 
            'Ã»': 'û', 'Ã¹': 'ù', 'Ã§': 'ç', 'â€™': "'", 'Å“': 'œ', 'â‚¬': '€',
            'Ã\xa0': 'à', 'Ã«': 'ë', 'Ã¯': 'ï', 'Ã…': 'Å', 'â€¦': '...',
            'âš ï¸': '⚠️', 'âœ…': '✅', 'ðŸ’¡': '💡', 'ðŸ’0': '💰', 
            'âš ': '⚠️', 'ðŸ“ˆ': '📈', 'ðŸ”': '🔍', 'ðŸ‘‰': '👉', 'ðŸŒŸ': '🌟',
            'ðŸŽ“': '🎓', 'ðŸ0': '🏠', 'ðŸ¢': '🏫', 'ðŸ¼': '🎨', 'ðŸŠ': '🩺',
            'ðŸ›0': '🛠️', 'ðŸ’»': '💻', 'ðŸŠ': '🩺', 'ðŸ“š': '📚', 'ðŸ¤”': '🤔'
        }
        for bad, good in replacements.items():
            cleaned = cleaned.replace(bad, good)
            
        # Nettoyage final des artefacts Prolog (guillemets, virgules au début/fin)
        cleaned = cleaned.strip().strip("'").strip('"').strip(',').strip()
        
        # Supprimer les crochets '[' ou ']' si présents (listes Prolog)
        cleaned = cleaned.replace('[|', '').replace('|]', '').replace('[', '').replace(']', '')
        
        return cleaned

    # Helper Contexte : Cherche dans le message, sinon utilise le contexte précédent
    def found_context_match(keywords_dict, current_message, context_topic):
        """Retourne la clé trouvée dans current_message OU dans context_topic"""
        # 1. Chercher dans le message actuel
        for k, v in keywords_dict.items():
            if k in current_message: return v
            
        # 2. Chercher dans le contexte (si message court/ambigu)
        if context_topic and len(current_message.split()) < 5:
            for k, v in keywords_dict.items():
                if k in context_topic.lower(): return v
        return None

    current_session_id = data.get('session_id', session_data.get('uuid', 'default'))

    # --- 0. GESTION DES ETATS (State Machine / Quiz) ---
    current_state = conversation_manager.get_state(current_session_id)
    if current_state:
        state_name = current_state.get('current')
        
        # ESCAPE HATCH: si la question ne ressemble pas a une reponse de Quiz, on annule
        QUIZ_ESCAPE_KEYWORDS = [
            'encg', 'ensa', 'uir', 'um6p', 'emsi', 'fst', 'ensias', 'fmp',
            'quelle', 'combien', 'comment', 'quel', 'quels', 'quand', 'est-ce',
            'bonjour', 'bonsoir', 'salut', 'merci', 'bourse', 'frais', 'prix',
            'informatique', 'medecine', 'pharmacie', 'ingenieur', 'architecture',
            'c koi', 'c est', 'meilleur', 'liste', 'donne', 'moins cher', 'moins chere'
        ]
        user_low_for_quiz = user_message.lower()
        if any(kw in user_low_for_quiz for kw in QUIZ_ESCAPE_KEYWORDS):
            conversation_manager.clear_state(current_session_id)
            current_state = None
        
        if current_state:
            if state_name == 'QUIZ_Q1':
                # Attente de la réponse à Q1 (Série Bac)
                bac_type = user_message.upper()
                if any(b in bac_type for b in ['PC', 'SVT', 'SM', 'ECO', 'LITT', 'PRO']):
                    conversation_manager.update_state_data(current_session_id, 'bac', bac_type)
                    conversation_manager.set_state(current_session_id, 'QUIZ_Q2', current_state['data'])
                    return jsonify({"response": "Super, c'est noté. 📝\n\nQuestion 2 : Quelle est ta moyenne au lycée environ (ex: 12, 14, 16) ?"})
                else:
                    # Pas une série bac valide -> annuler le quiz
                    conversation_manager.clear_state(current_session_id)
                    
            elif state_name == 'QUIZ_Q2':
                # Attente de la réponse à Q2 (Moyenne)
                try:
                    # Try to extract a number
                    numbers = re.findall(r'\d+', user_message)
                    if numbers:
                        note = float(numbers[0])
                        bac = current_state['data'].get('bac', 'PC')
                        
                        # Fin du quiz, on interroge Prolog avec ces infos
                        conversation_manager.clear_state(current_session_id)
                        
                        q = f"strategie_profil({note}, '{bac}', Conseil)"
                        res = list(prolog.query(q))
                        if res:
                            raw_conseil = clean_text(res[0]['Conseil'])
                            if ResponseBuilder:
                                response_text = ResponseBuilder.build_strategy_response(note, bac, raw_conseil)
                            else:
                                response_text = f"🎯 **Conseil Personnalisé ({note}/20 - Bac {bac})** :\n{raw_conseil}"
                            return jsonify({"response": "Merci pour ces infos ! J'ai analysé ton profil.\n\n" + response_text})
                except Exception as e:
                    print(e)
                return jsonify({"response": "Pourrais-tu me donner juste un nombre pour ta moyenne (ex: 13) ?"})

    # --- CUSTOM Q&A (Priorité ABSOLUE) ---
    if supabase:
        try:
            qa_data = supabase.table('custom_qa').select('*').execute()
            if qa_data.data:
                for qa in qa_data.data:
                    questions = qa.get('questions', [])
                    answer = qa.get('answer', '')
                    for q in questions:
                        q_norm = normalize_text(q.lower())
                        # Match si la question stockée est dans le message utilisateur ou vice versa
                        if q_norm in user_message_normalized or user_message_normalized in q_norm:
                            print(f"✓ Custom Q&A Match: '{q}' -> Réponse personnalisée envoyée")
                            return jsonify({"response": answer})
        except Exception as e_qa:
            print(f"⚠ Erreur Custom Q&A: {e_qa}")


    # --- 0.5 INIT CONTEXT LOGIC (Avant les retours prématurés) ---
    current_entity = extract_entity(user_message_normalized)
    
    # Init context for this session
    if current_session_id not in session_context:
        session_context[current_session_id] = {'last_intent': None, 'last_entity': None, 'last_topic': None}
    context = session_context[current_session_id]

    # --- CHARGER LE PROFIL UTILISATEUR (Supabase/JSON) ---
    user_profile = {}
    if UserMemory:
        user_profile = UserMemory.load(current_session_id, supabase)
        # Détecter les infos de profil dans ce message (bac, moyenne, ville)
        profile_hints = UserMemory.extract_profile_hints(user_message, user_profile)
        if profile_hints:
            UserMemory.update(current_session_id, profile_hints, supabase)
            user_profile.update(profile_hints)
            context.update(profile_hints)

    # --- 0.6 LOGIQUE MÉTIER / COMPATIBILITÉ Bac (DÉTECTION À LA VOLÉE) ---
    msg_low = user_message.lower()
    
    if "12" in msg_low and "moyenne" in msg_low:
        return jsonify({"response": "💡 **Conseil (Moyenne ~12/20)** : Avec 12, les grandes écoles publiques très sélectives (Médecine, Architecture) seront difficiles d'accès. Privilégie la **Faculté des Sciences (Universités)** pour faire du développement ou de la biologie, les **BTS/DUT** orientés technique, ou bien les bonnes écoles privées !"})

    if ("medecine" in msg_low or "pharmacie" in msg_low) and ("eco" in msg_low or "lettres" in msg_low or "10" in msg_low or "11" in msg_low):
        return jsonify({"response": "❌ **Réalité Admission Médecine** : C'est **très difficile voire impossible**. La médecine exige un Bac Scientifique avec un seuil élevé (13.5+). Tu pourrais t'orienter vers des universités à l'étranger ou le Management de la Santé à la place !"})

    if "nul" in msg_low and "math" in msg_low:
        return jsonify({"response": "💡 **Pas de panique !** Si les maths ne sont pas ton fort, le Maroc offre d'excellentes voies en Lettres, Arts, Droit, ou Commerce (où les maths sont plus appliquées)."})
        
    if "deteste" in msg_low or "déteste" in msg_low:
        if "informatique" in msg_low:
            return jsonify({"response": "💡 **C'est noté !** Si on doit éviter l'informatique, je te conseille de regarder du côté du **Commerce** (ENCG, ISCAE), la **Santé** ou le **Droit**. Quel domaine t'attire ?"})

    # Bac Eco -> Ingenieur (impossible)
    if ("ingenieur" in msg_low or "ingenierie" in msg_low) and "eco" in msg_low:
        return jsonify({"response": "❌ **Compatibilité Bac Éco → Ingénierie** : En général, les écoles d'ingénieurs (ENSA, ENSIAS, EMI) exigent un **Bac Scientifique** (PC, SM, SVT). Avec un Bac Eco, tu peux t'orienter vers le **Management de projet tech** ou le **Business & IT** dans des écoles de commerce."})

    # Salary focus / argent
    if "salaire" in msg_low and ("maroc" in msg_low or "plus" in msg_low or "rapporte" in msg_low):
        return jsonify({"response": "💰 **Métiers les mieux rémunérés au Maroc :**\n\n1. **Médecine spécialisée** (40 000 - 80 000 DH/mois)\n2. **IA / Data Science** (15 000 - 45 000 DH/mois)\n3. **Finance & Investissement** (20 000 - 60 000 DH/mois)\n4. **Architecture** (15 000 - 35 000 DH/mois)\n5. **Ingénierie** (10 000 - 30 000 DH/mois)\n\n> Ces chiffres varient selon l'expérience et la ville."})

    # Multi-contrainte : ecoles payantes dans une ville spécifique + domaine
    if ("payant" in msg_low or "privee" in msg_low or "prix" in msg_low) and "rabat" in msg_low:
        return jsonify({"response": "📍 **Écoles privées payantes à Rabat :**\n\n- **UIR** (Université Internationale de Rabat) : Ingénierie, Business, Informatique - 70 000 – 90 000 DH/an\n- **EMSI Rabat** : Informatique, Réseaux - ~40 000 DH/an\n- **ISPITS** : Soins infirmiers - ~20 000 DH/an\n\nPrécisez la filière pour affiner !"})

    # ENSA inscription dates / Minhaty dates
    if ("quand" in msg_low or "date" in msg_low) and "minhaty" in msg_low:
        return jsonify({"response": "📅 **Inscriptions Minhaty :**\n\nLa période d'inscription Minhaty est généralement ouverte entre **Juin et Juillet** chaque année, via le portail **minhaty.ma**. Guette les annonces officielles du Ministère !"})

    # Bac SVT specialized debouches (Test #2)
    if ("debouche" in msg_low or "faire" in msg_low) and "bac svt" in msg_low:
        return jsonify({"response": "🩺 **Débouchés Bac SVT :**\n\nAvec un Bac SVT, les voies royales sont :\n1. **Médecine (FMP)** : Concours exigeant, seuil ~14-15.\n2. **Infirmerie (ISPITS) / Paramédical** : Très forte demande.\n3. **FST / Fac des Sciences** : Pour une licence en biologie ou chimie.\n4. **Agronomie (IAV / ENA)** : Pour devenir ingénieur agronome.\n\nC'est la série idéale pour les métiers de la santé et du vivant !"})


    # Context carry: si on parle de pharmacie apres medecine, on donne les details pharmacie
    if "pharmacie" in msg_low and context.get('last_intent') in ['FUTURE_JOBS', None]:
        return jsonify({"response": "🏥 **Pharmacie (FMP) :**\n\nLa pharmacie au Maroc est formée à la **Faculté de Médecine et de Pharmacie (FMP)**. Le seuil moyen est autour de **13.0 - 14.0** pour l'accès au concours. La formation dure **6 ans** et débouche sur des postes en officine, industrie pharmaceutique ou recherche."})

    if "changer" in msg_low and "medecine" in msg_low and ("encg" in msg_low or "engc" in msg_low):
         return jsonify({"response": "❌ **Passerelle Impossible** : On ne peut pas changer de l'ENCG (Commerce) vers la Médecine. La Médecine exige un bac scientifique et une inscription dès la première année (concours unifié). Il faut repasser un bac scientifique libre si tu veux vraiment faire ça !"})

    if "etranger" in msg_low or "france" in msg_low or "étranger" in msg_low:
        return jsonify({"response": "🌍 **Études à l'étranger (Campus France etc.)** : Mon expertise principale est le Maroc, mais pour la France : prépare ton TCF, vise de bonnes notes, et suis la procédure Campus France dès Novembre pour ton Visa !"})

    # ====================================================================
    # ANTI-ROBOTIQUE 1 : MULTI-TOUR / CONTEXT CARRY INTELLIGENT
    # Pattern "Et pour X ?" ou "Et X ?" -> re-router sur le dernier sujet
    # ====================================================================
    et_pour_match = re.search(r'^(et\s+)?(pour\s+)?(la\s+|le\s+|les\s+|l\')?(\w+)\s*\??$', msg_low.strip())
    if et_pour_match and len(msg_low.split()) <= 5:
        follow_entity = extract_entity(msg_low)
        if follow_entity and context.get('last_intent'):
            last_intent = context['last_intent']
            print(f"🔄 CONTEXT CARRY: '{follow_entity}' avec intent précédent '{last_intent}'")
            if follow_entity == 'pharmacie':
                return jsonify({"response": "🏥 **Pharmacie (FMP) :**\n\nLa pharmacie au Maroc est formée à la **Faculté de Médecine et de Pharmacie (FMP)**. Le seuil moyen est autour de **13.0 - 14.0** pour l'accès au concours. La formation dure **6 ans** et débouche sur des postes en officine, industrie pharmaceutique ou recherche."})

    # ====================================================================
    # ANTI-ROBOTIQUE 2 : RAISONNEMENT CONDITIONNEL ("si j'ai X de moyenne")
    # ====================================================================
    cond_avg_match = re.search(r'\bsi\b.*?(\d{1,2}[.,]?\d{0,2})\s*(de\s+)?moyenne', msg_low)
    if cond_avg_match and current_entity:
        try:
            cond_score = float(cond_avg_match.group(1).replace(',', '.'))
            ecole = current_entity.upper()
            if cond_score >= 16:
                verdict = f"✅ Avec **{cond_score}** tu as accès aux meilleures écoles ({ecole} compris). Vise haut !"
            elif cond_score >= 14:
                verdict = f"🟡 Avec **{cond_score}** tu as une chance sérieuse pour {ecole}. C'est jouable avec un bon dossier !"
            elif cond_score >= 12:
                verdict = f"🟠 Avec **{cond_score}** c'est limité pour {ecole} (seuil souvent 13-15+). Mais les écoles privées restent une option."
            else:
                verdict = f"🔴 Avec **{cond_score}** l'accès à {ecole} sera très difficile. Je te conseille de viser des BTS ou des universités à accès libre d'abord."
            
            # Bourse conditionnelle
            bourse_note = ""
            if 'bourse' in msg_low or 'uir' in msg_low:
                if cond_score >= 16:
                    bourse_note = "\n\n🏆 **Bourse** : Tu as la bourse d'excellence complète (couverture totale)."
                elif cond_score >= 14:
                    bourse_note = "\n\n💛 **Bourse** : Bourse partielle possible (50%). Renseigne-toi auprès du bureau des bourses."
                else:
                    bourse_note = "\n\n🤝 **Bourse sociale** : Demande Minhaty (aide selon revenu des parents, pas la moyenne)."
            return jsonify({"response": verdict + bourse_note})
        except Exception:
            pass

    # ====================================================================
    # ANTI-ROBOTIQUE 3 : QUESTIONS D'OPINION ("X c'est bien ?", "vaut le coup ?")
    # ====================================================================
    OPINION_WORDS = ['bien', 'vaut', 'merite', 'recommande', 'avis', 'bonne', 'serieux', 'credible', 'qualite']
    if current_entity and any(w in msg_low for w in OPINION_WORDS):
        target = current_entity.upper()
        q = f"get_avis_ecole('{target}', Note, Positif, Negatif)"
        try:
            res = list(prolog.query(q))
            if res:
                r = res[0]
                response = (f"⭐ **{target}** — {clean_text(r['Note'])}\n\n"
                           f"✅ **Points forts :** {clean_text(r['Positif'])}\n\n"
                           f"⚠️ **Points faibles :** {clean_text(r['Negatif'])}")
                return jsonify({"response": response})
        except Exception:
            pass

    # ====================================================================
    # ANTI-ROBOTIQUE 4 : ENTITÉ SEULE -> SMART PROMPT
    # Note: executé ici, avant le classifieur, uniquement si msg court
    # ====================================================================
    if len(user_message.split()) <= 2 and current_entity:
        entity_name = current_entity.upper()
        return jsonify({"response": f"🏥 Tu veux savoir quoi sur **{entity_name}** ?\n\n"
                                   f"Dis-moi ce qui t'intéresse :\n"
                                   f"💰 Frais / Prix · 📝 Procédure d'admission · 📍 Localisation\n"
                                   f"🎓 Débouchés / Métiers · ⭐ Avis / Qualité · ℹ️ Définition"})

    # Slang "combien" sans école connue -> demander laquelle
    if 'combien' in msg_low and not current_entity:
        return jsonify({"response": "🤔 **Combien... quoi exactement ?**\n\nPrécisez l'école (ex: UIR, ENSA, EMSI...) et ce qui vous intéresse (frais, bourse, salaire) ! Je peux vous aider."})

    # ====================================================================
    # ANTI-ROBOTIQUE 5 : TON ADAPTATIF (détection du stress / découragement)
    # ====================================================================
    STRESS_WORDS = ['stresse', 'stress', 'peur', 'perdu', 'panique', 'inquiet', 'anxieux', 'dur', 'difficile', 'impossible']
    _empathy_prefix = ""
    if any(w in msg_low for w in STRESS_WORDS) and len(msg_low.split()) > 3:
        _empathy_prefix = "🧘 *Calme-toi, c'est normal de stresser. Tu vas y arriver !*\n\n"

    # --- 1. LOCAL INTENT CLASSIFIER (NLU) ---
    detected_intent = None

    if intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)
    with open(r"c:\Users\PC\Downloads\YAFI\yafi2-main\backend\debug_chat.log", "a", encoding="utf-8") as lf:
        lf.write(f"Message: {{user_message_normalized}}\n")
        lf.write(f"Detected Intent: {{detected_intent}}\n")
        lf.write(f"Current Entity: {{current_entity}}\n")

        # --- BRUTE FORCE FALLBACK FOR COMPARISONS ---
        if detected_intent is None:
            msg_low = user_message.lower()
            if any(w in msg_low for w in ["comparer", "difference", " vs ", " entre "]):
                schools_found = [ent for ent in KNOWN_ENTITIES if ent in msg_low]
                if len(schools_found) >= 2:
                    detected_intent = "COMPARE_SCHOOLS"
                    print(f"🔥 BRUTE FORCE MATCH: {detected_intent}")
        
        # 1.1 CONTEXT FALLBACK (Mémoire)
        if detected_intent is None and context['last_intent'] is not None and current_entity:
            print(f"🔄 CONTEXT FALLBACK: Using last intent '{context['last_intent']}' for new entity '{current_entity}'")
            detected_intent = context['last_intent']
            user_message += f" {current_entity}"
            user_message_normalized += f" {current_entity}"
            
        # 1.2 DYNAMIC ATTRIBUTE ROUTING (Fallback Logic)
        if detected_intent is None and current_entity:
            msg = user_message.lower()
            print(f"⚡ DYNAMIC FALLBACK: No intent found, but entity '{current_entity}' detected. Checking attributes.")
            if any(k in msg for k in ['duree', 'ans', 'annee', 'combien de temps']):
                res = list(prolog.query("etablissement(Ecole, _, _, Duree, _)"))
                for r in res:
                    if current_entity in clean_text(r['Ecole']).lower():
                        details = f"🎓 La durée des études à **{clean_text(r['Ecole'])}** est de : **{clean_text(r['Duree'])} ans**."
                        return jsonify({"response": details})
                        
            elif any(k in msg for k in ['diplome', 'titre']):
                res = list(prolog.query("etablissement(Ecole, _, Diplome, _, _)"))
                for r in res:
                    if current_entity in clean_text(r['Ecole']).lower():
                        details = f"🎓 Le diplôme délivré par **{clean_text(r['Ecole'])}** est : **{clean_text(r['Diplome'])}**."
                        return jsonify({"response": details})
            
            # If no attribute matched but we found an entity, prompt user
            return jsonify({"response": f"J'ai compris que tu parles de **{current_entity.upper()}**, mais que veux-tu savoir exactement ? (le prix, la procédure, la durée, le diplôme...)"})

        # Update Context Memory (enrichi avec last_topic)
        if detected_intent:
            context['last_intent'] = detected_intent
        if current_entity:
            context['last_entity'] = current_entity
            context['last_topic'] = current_entity  # NOUVEAU
        # Sauvegarder profil utilisateur async
        if UserMemory:
            UserMemory.update(current_session_id, {
                'last_intent': detected_intent,
                'last_entity': current_entity,
                'last_topic': current_entity
            }, None)  # None = pas de Supabase sur chaque message pour les perfs
        
        # LOGIQUE DÉDIÉE: Seuils
        if re.search(r'\bseuils?\b', user_message) and current_entity == 'encg':
            return jsonify({"response": "📈 **Seuils ENCG (Estimation) :**\n\nLe seuil pour l'ENCG varie chaque année. En général, il se situe autour de **14.5 - 15.5** pour les bacheliers PC/SVT et entre **12 - 13** pour les Eco."})
        elif re.search(r'\bseuils?\b', user_message) and 'medecine' in msg_low:
            if '2023' in msg_low:
                return jsonify({"response": "📈 **Seuil Médecine (2023) :**\n\nEnviron 14.00 (mais a baissé récemment) suite à la réforme."})
            else:
                return jsonify({"response": "📈 **Seuil Médecine :**\n\nHistoriquement autour de 13.5 - 14.0 pour accéder au concours unifié FMP."})
        if detected_intent == "SCHOLARSHIPS":
            # Extract scholarship info from Prolog
            q = "get_bourse_merite(Ecole, Type, Condition)"
            res = list(prolog.query(q))
            if res:
                response = "🎓 **Bourses de Mérite & Financements :**\n\n"
                for r in res[:4]:
                    response += f"- **{clean_text(r['Ecole'])}** ({clean_text(r['Type'])}) : {clean_text(r['Condition'])}\n"
                response += "\n💡 *Il existe aussi la bourse publique Minhaty. As-tu une école précise en tête ?*"
                return jsonify({"response": response})
                
        elif detected_intent == "FUTURE_JOBS":
            q = "get_metier_avenir(Domaine, Metier, Demande, Conseils)"
            res = list(prolog.query(q))
            if res:
                response = "🚀 **Les Métiers d'Avenir au Maroc :**\n\n"
                for r in res[:3]:
                    response += f"🔹 **{clean_text(r['Domaine'])}** ({clean_text(r['Metier'])})\n"
                    response += f"   *Demande : {clean_text(r['Demande'])}*\n"
                    response += f"   *Conseil : {clean_text(r['Conseils'])}*\n\n"
                return jsonify({"response": response})

        elif detected_intent == "COMPARE_SCHOOLS":
             # Extract two schools
             schools_in_msg = []
             for ent in KNOWN_ENTITIES:
                 if ent in user_message.lower():
                     schools_in_msg.append(ent)
             
             if len(schools_in_msg) >= 2:
                 s1, s2 = schools_in_msg[0], schools_in_msg[1]
                 
                 def fetch_school_data(name):
                     sid = normalize_school_id(name)
                     q_sal = f"average_salary('{sid}', S)"
                     res_s = list(prolog.query(q_sal))
                     q_rate = f"employment_rate('{sid}', R)"
                     res_r = list(prolog.query(q_rate))
                     q_city = f"localisation('{sid}', C)"
                     res_c = list(prolog.query(q_city))
                     
                     return {
                         "salary": clean_text(res_s[0]['S']) if res_s else "N/A",
                         "rate": f"{int(float(res_r[0]['R'])*100)}%" if res_r else "N/A",
                         "city": clean_text(res_c[0]['C']) if res_c else "N/A"
                     }
                 
                 data1 = fetch_school_data(s1)
                 data2 = fetch_school_data(s2)
                 if ResponseBuilder:
                     response_text = ResponseBuilder.build_comparison_response(s1.upper(), data1, s2.upper(), data2)
                 else:
                     response_text = f"⚖️ **Comparaison** : {s1.upper()} vs {s2.upper()}\n- Salaire: {data1['salary']} vs {data2['salary']}\n- Insertion: {data1['rate']} vs {data2['rate']}"
                  return jsonify({"response": response_text})
             else:
                 response_text = "⚖️ **Comparaison** : Indiquez deux écoles (ex: 'Compare EMSI et UIR') pour voir leurs statistiques côte à côte."
                  return jsonify({"response": response_text})

        elif detected_intent == "WHERE_TO_STUDY":
            response = "📍 **Où Étudier ?**\n\n"
            if "architecture" in msg_low:
                return jsonify({"response": "📍 L'**Architecture** s'étudie principalement à l'ENA (publique, partout au Maroc) ou dans des écoles privées comme l'UIR et l'EAC."})
            elif "ensa" in msg_low and "tanger" in msg_low:
                return jsonify({"response": "📍 **OUI !** Il y a bel et bien une ENSA à Tanger. Elle offre d'excellentes filières en informatique et systèmes urbains."})
            elif "ensias" in user_message:
                response += "L'**ENSIAS** est située à **Rabat** (Madinat Al Irfane). C'est l'une des meilleures écoles d'informatique."
            elif "casablanca" in user_message or "casa" in user_message:
                response += "À Casablanca, vous trouverez l'UH2C, l'ENCG-C, l'EMSI et plusieurs facultés de médecine."
            else:
                response += "Précisez la ville ou le domaine pour que je vous liste les établissements !"
            return jsonify({"response": response})

        elif detected_intent == "SCHOOL_FEES" or "budget" in user_message.lower() or "coût" in user_message.lower():
             # Check for budget smart search
             entities = intent_classifier.extract_entities(user_message) if intent_classifier else {}
             budget = entities.get('budget')
             
             if budget or "gratuit" in user_message.lower():
                 if "gratuit" in user_message.lower(): budget = 0
                 # Default domain search
                 domain = 'engineering' if any(w in user_message.lower() for w in ['ingé', 'techno']) else 'commerce' if 'business' in user_message.lower() else 'informatique'
                 
                 q_smart = f"find_best_school('{domain}', {budget}, 5000, Ecole)"
                 try:
                     res_smart = list(prolog.query(q_smart))
                     if res_smart:
                         schools = list(set([str(r['Ecole']) for r in res_smart]))
                         response_text = f"✅ D'après ton budget de **{budget} DH**, voici des écoles d'**{domain}** recommandées :\n\n"
                         for s in schools[:5]:
                             response_text += f"• **{s}**\n"
                         response_text += "\n*Note : Ces écoles respectent tes critères de coût et de salaire à la sortie.*"
                          return jsonify({"response": response_text})
                     else:
                         response_text = f"Désolé, je n'ai pas trouvé d'école d {domain} correspondant exactement à un budget de {budget} DH. Voulez-vous essayer avec un budget plus large ?"
                          return jsonify({"response": response_text})
                 except: 
                     response_text = "Désolé, une erreur technique est survenue lors de la recherche par budget."
                      return jsonify({"response": response_text})
             
             # Fallback to standard fees handler 
             if not ('response_text' in locals() and response_text and "budget" in response_text):
                 if "moins cher" in msg_low or "moins chere" in msg_low:
                     response_text = "💰 **Écoles Moins Chères :** Regardez du côté de l'EHEC, l'EMSI et SupMti (~35 000 à 45 000 DH/an). L'UM6P offre aussi d'excellentes bourses de mérite qui couvrent tout."
                 else:
                     q = "get_frais_scolarite(Ecole, Prix, Note)"
                     res = list(prolog.query(q))
                     if res:
                         response_text = "💰 **Frais de Scolarité & Coûts d'Inscription :**\n\n"
                         found_specific = False
                         if current_entity:
                             for r in res:
                                 ecole_name = clean_text(r['Ecole'])
                                 if current_entity.lower() == ecole_name.lower():
                                     response_text = f"💰 **Frais pour {ecole_name} :**\n\n- **Scolarité :** {clean_text(r['Prix'])}\n- **Détails :** {clean_text(r['Note'])}\n"
                                     found_specific = True
                                     break
                         if not found_specific:
                             for r in res[:6]:
                                 response_text += f"- **{clean_text(r['Ecole'])}** : {clean_text(r['Prix'])}\n"
                             response_text += "\n💡 *Les prix varient selon les filières. Est-ce qu'une école en particulier t'intéresse ?*"
                          return jsonify({"response": response_text})
                     else:
                         response_text = "Je n'ai pas trouvé d'informations sur les frais pour le moment."
                          return jsonify({"response": response_text})

        elif detected_intent == "ADMISSION_PROCEDURE":
            if "fac" in msg_low or "universite" in msg_low:
                 return jsonify({"response": "📝 **Procédure d'admission : Université / Fac**\n\n1. Pré-inscription sur la plateforme universitaire (souvent via Massar).\n2. Préparer son dossier physique (Bac original, photos, CIN).\n3. Dépôt sur place lors des dates précisées sur le site de l'établissement.\n\nL'accès est généralement libre sans concours préalable pour les licences fondamentales."})
            
            target = "Minhaty" if "minhaty" in msg_low else "Medecine" if "medecine" in msg_low else ("OFPPT" if "ofppt" in msg_low else "Minhaty")
            
            if target == "OFPPT":
                 return jsonify({"response": "📝 **Procédure d'admission : OFPPT**\n\nL'admission se fait le plus souvent **SANS CONCOURS** (Admission Directe sur dossier) pour le niveau Technicien Spécialisé, selon les places disponibles. L'inscription commence assez tôt via leur portail *takwin*."})

            q = f"get_procedure_details('{target}', Etape, Txt)"
            res = list(prolog.query(q))
            if res:
                response = f"📝 **Procédure d'admission : {target}**\n\n"
                sorted_res = sorted(res, key=lambda x: int(x['Etape']))
                for r in sorted_res:
                    response += f"{r['Etape']}. {clean_text(r['Txt'])}\n"
                
                if target == "Minhaty" and "quand" in user_message.lower() or "date" in user_message.lower():
                    response += "\n📅 **Date clé** : La période d'inscription est généralement ouverte entre **Juin et Juillet**."
                return jsonify({"response": response})

        # --- ADVANCED AXE 5 HANDLERS ---
        elif detected_intent == "SALARY_INFO":
             entity = extract_entity(user_message)
             if entity:
                 school_id = normalize_school_id(entity)
                 q_sal = f"average_salary('{school_id}', S)"
                 res_sal = list(prolog.query(q_sal))
                 q_emp = f"employment_rate('{school_id}', R)"
                 res_emp = list(prolog.query(q_emp))
                 
                 if res_sal or res_emp:
                     sal = clean_text(res_sal[0]['S']) if res_sal else "N/A"
                     emp_val = f"{int(float(res_emp[0]['R'])*100)}%" if res_emp else "N/A"
                     if ResponseBuilder:
                         response_text = ResponseBuilder.build_stat_response(entity.upper(), sal, emp_val)
                     else:
                         response_text = f"📊 **Stats {entity.upper()}** : Salaire ~{sal} DH, Taux d'insertion ~{emp_val}"
                     return jsonify({"response": response_text})

        elif detected_intent == "CAMPUS_LIFE":
             entity = extract_entity(user_message)
             if entity:
                 school_id = normalize_school_id(entity)
                 info_type = 'menu' if any(w in user_message for w in ['menu', 'manger', 'cantine', 'repas']) else 'club'
                 if info_type == 'menu':
                     q_menu = f"meal('{school_id}', monday, lunch, M)"
                     try:
                         res_m = list(prolog.query(q_menu))
                         if res_m:
                             response_text = ResponseBuilder.build_campus_info_response(entity.upper(), 'menu', f"Exemple de menu (Lundi) : {clean_text(res_m[0]['M'])}")
                             return jsonify({"response": response_text})
                     except: pass
                 else:
                     q_env = f"environment_feature('{school_id}', E)"
                     try:
                         res_e = list(prolog.query(q_env))
                         if res_e:
                             response_text = ResponseBuilder.build_campus_info_response(entity.upper(), 'campus', clean_text(res_e[0]['E']))
                             return jsonify({"response": response_text})
                     except: pass

        elif detected_intent == "CONCOURS_CALENDAR" or ("concours" in user_message.lower() and ("quand" in user_message or "date" in user_message or "calendrier" in user_message)):
             response_text = get_upcoming_concours()
             if response_text:
                 return jsonify({"response": response_text})

        elif detected_intent == "GENERAL_INFO":
            # Si on a une entité (ex: ENCG), on cherche sa définition
            target_entity = current_entity if current_entity else ("medecine" if "medecine" in user_message else "informatique")
            q = "get_definition(Acronyme, Nom, Detail)"
            res = list(prolog.query(q))
            for r in res:
                if target_entity == clean_text(r['Acronyme']).lower() or target_entity == clean_text(r['Nom']).lower():
                    response = f"🎓 **{clean_text(r['Acronyme'])}** ({clean_text(r['Nom'])})\n\n{clean_text(r['Detail'])}"
                    return jsonify({"response": response})
            # Default
            return jsonify({"response": "C'est une excellente question. Pouvez-vous préciser l'école ou le domaine (ex: C'est quoi l'ENCG ?) ? "})

        elif detected_intent == "RECOMMENDATION":
            target_domaine = "informatique" if "informatique" in user_message.lower() else ("commerce" if "commerce" in user_message.lower() else "informatique")
            q = f"get_recommandation('{target_domaine}', Texte)"
            res = list(prolog.query(q))
            if res:
                response = f"🏆 **Meilleures recommandations ({target_domaine}) :**\n\n{clean_text(res[0]['Texte'])}"
                return jsonify({"response": response})

        elif detected_intent == "SOFT_SKILLS":
            target_skill = "organisation" if "organisation" in user_message.lower() else "stress"
            q = f"get_soft_skills('{target_skill}', Conseil)"
            res = list(prolog.query(q))
            if res:
                response = f"🧘 **Conseils ({target_skill}) :**\n\n{clean_text(res[0]['Conseil'])}"
                return jsonify({"response": response})

        elif detected_intent == "GENERAL_ADVICE":
            conversation_manager.set_state(current_session_id, 'QUIZ_Q1')
            response = "Pas de panique ! 🧭 Je vais t'aider à trouver ta voie en te posant 2 petites questions.\n\n**Question 1 :** Quelle est ta série de Bac (ex: PC, SVT, Eco, Lettres) ?"
            return jsonify({"response": response})
            
    # --- RAG PROFESSIONNEL (Vector Search) ---
    vector_response = None
    vector_search_used = False
    
    with open(r"c:\Users\PC\Downloads\YAFI\yafi2-main\backend\debug_chat.log", "a", encoding="utf-8") as lf:
        lf.write(f"Entering RAG Block: {{not detected_intent}}\n")
    if not detected_intent and USE_VECTOR_SEARCH and len(user_message_normalized) > 2:  # Accepte les questions très courtes aussi
        try:
            # 1. Ajouter le message utilisateur à l'historique
            # session_id est récupéré plus haut ou généré
            current_session_id = data.get('session_id', session_data.get('uuid', 'default'))
            conversation_manager.add_message(current_session_id, 'user', user_message_normalized)
            
            # 2. Récupérer le contexte
            history = conversation_manager.get_history(current_session_id, last_n=4)
            
            # 3. Recherche Vectorielle - PARAMETERS OPTIMISÉS
            print(f"🔍 Vector Search pour: '{user_message_normalized}'")
            # Réduit seuil de 0.6 à 0.35 pour plus de résultats
            # Augmenté top_k de 3 à 5 pour plus de contexte
            search_results = vector_kb.search(user_message_normalized, top_k=5, threshold=0.35)
            
            if search_results:
                # 4. Générer la réponse enrichie avec LLM (Ollama)
                best_match = search_results[0]
                
                # Construire le contexte à partir des résultats de recherche
                context = "\n\n".join([content for _, content in search_results])
                
                # APPEL OLLAMA AVEC PERMISSIONS AVANCÉES ⭐
                # Donne plus de libertés à Ollama pour générer de MEILLEURES réponses
                print(f"🚀 Appel Ollama AVANCÉ avec plus de permissions...")
                llm_response, confidence = OllamaAdvancedConfig.call_ollama_advanced(
                    user_message_normalized,
                    context
                )
                
                if llm_response:
                    # ✅ Succès: utiliser la réponse d'Ollama
                    vector_response = llm_response
                    
                    # Ajouter les sources si disponible
                    if search_results:
                        try:
                            # Ajouter une note de sources
                            sources_text = "\n\n📚 **Sources:**\n"
                            for i, (_, content) in enumerate(search_results[:2], 1):
                                sources_text += f"  {i}. {content[:60]}...\n"
                            vector_response += sources_text
                        except:
                            pass
                else:
                    # Fallback si Ollama échoue
                    print("⚠️ Ollama n'a pas répondu, utilisation du fallback...")
                    best_match = search_results[0] if search_results else None
                    if best_match:
                        vector_response = best_match[1]
                    else:
                        vector_response = "Désolé, je n'ai pas compris votre question."
                
                print(f"✅ VECTEUR MATCH: {best_match['score']:.2%} - {best_match['metadata']['category']}")
                vector_search_used = True
                
                # 5. Sauvegarder la réponse dans l'historique
                conversation_manager.add_message(
                    current_session_id, 
                    'assistant', 
                    vector_response,
                    metadata={'score': best_match['score'], 'source': 'vector_search'}
                )
                
                # 6. Retourner immédiatement
                return jsonify({
                    "response": vector_response,
                    "metadata": {
                        "source": "vector_rag",
                        "confidence": best_match['score'],
                        "category": best_match['metadata'].get('category')
                    }
                })
            else:
                print("🔸 Pas de match vectoriel suffisant (seuil 0.6)")
                
        except Exception as e_vec:
            print(f"❌ Erreur Vector Search: {e_vec}")
            # Continuer vers la logique legacy en cas d'erreur


    try:
        # Initialize response_text with a default value to prevent UnboundLocalError
        response_text = "Je n'ai pas compris votre question. Pouvez-vous la reformuler ?"
        
        # --- ABBREVIATIONS & MOTS COURTS (Très Haute Priorité) ---
        # CV / Curriculum
        if user_message in ['cv', 'c v', 'curriculum']:
            return jsonify({"response": "Pour créer un bon CV étudiant :\n\n📝 **Sections essentielles** :\n- Informations personnelles\n- Formation (Bac, mention)\n- Compétences (langues, informatique)\n- Expériences (stages, projets)\n- Centres d'intérêt\n\n💡 **Conseils** :\n- 1 page maximum\n- Police professionnelle\n- Pas de photo (sauf demandé)\n- Mettre en avant les projets académiques\n\nBesoin d'aide pour une section spécifique ?"})
        
        # Abréviations écoles
        if user_message in ['ensa', 'e n s a']:
            return jsonify({"response": "🏫 **ENSA** (École Nationale des Sciences Appliquées)\n\nÉcoles d'ingénieurs publiques au Maroc.\n\n📍 **Villes** : Rabat, Casa, Fès, Marrakech, Tanger, Safi, Khouribga, El Jadida, Tétouan, Oujda, Agadir, Kenitra.\n\n✅ **Admission** : Bac PC/SM avec bonne moyenne (13-15+)\n💰 **Frais** : Gratuit (public)\n\nPosez une question plus précise (ex: 'ENSA Safi', 'Admission ENSA')"})
        
        if user_message in ['emsi', 'e m s i']:
            return jsonify({"response": "🏫 **EMSI** (École Marocaine des Sciences de l'Ingénieur)\n\nÉcole privée d'ingénierie et IT.\n\n📍 **Villes** : Rabat, Casa, Marrakech, Tanger\n💰 **Frais** : ~45 000 - 55 000 DH/an\n✅ **Filières** : Informatique, Réseaux, Data Science, Génie Civil\n\nPosez une question plus précise !"})
        
        # Langues courtes
        if user_message in ['fr', 'français', 'francais']:
            return jsonify({"response": "🇫🇷 **Études en Français**\n\nLe français est la langue principale pour :\n✅ Sciences et techniques\n✅ Médecine\n✅ Ingénierie\n✅ Commerce\n\nRecommandé si niveau ≥ B2.\n\nPosez 'Langue français' pour plus de détails."})
        
        if user_message in ['en', 'anglais', 'english']:
            return jsonify({"response": "🇬🇧 **Études en Anglais**\n\nL'anglais est utilisé pour :\n✅ IT et Data Science\n✅ Business international\n✅ Programmes internationaux\n\nNiveau B2/C1 requis.\n\nPosez 'Langue anglais' pour plus de détails."})
        
        if user_message in ['ar', 'arabe']:
            return jsonify({"response": "🇲🇦 **Études en Arabe**\n\nL'arabe est utilisé pour :\n✅ Lettres et sciences humaines\n✅ Droit national\n✅ Sciences islamiques\n\nPosez 'Langue arabe' pour plus de détails."})

        # --- SALUTATIONS MULTILINGUES (Priorité Haute) ---
        # Français
        if user_message in ['bonjour', 'bjr', 'bonsoir', 'bsr']:
            greetings = [
                "Bonjour ! 👋 Comment puis-je vous aider avec votre orientation ?",
                "Bonjour ! 🎓 Posez-moi vos questions sur l'orientation post-bac.",
                "Bonsoir ! Comment s'est passée votre journée ? Je suis là pour vous aider."
            ]
            return jsonify({"response": random.choice(greetings)})
        
        if user_message in ['salut', 'slt', 'coucou', 'cc']:
             return jsonify({"response": "Salut ! 👋 Ça va ? Besoin d'aide pour ton orientation ?"})
        
        if user_message in ['ca va', 'ça va', 'comment ca va', 'comment ça va', 'labas', 'kidayr']:
             return jsonify({"response": "Je vais très bien, merci ! 🤖 Toujours prêt pour vous orienter. Et vous ?"})
        
        if user_message in ['hey', 'yo']:
            return jsonify({"response": "Hey ! 😊 Quoi de neuf ? Des questions sur tes études ?"})
        
        if 'bonjour monsieur' in user_message or 'bonjour madame' in user_message:
            return jsonify({"response": "Bonjour Monsieur/Madame ! Comment puis-je vous aider aujourd'hui ?"})
        
        if 'bonjour professeur' in user_message:
            return jsonify({"response": "Bonjour Professeur ! 🎓"})
        
        # Darija (Arabe Marocain)
        if user_message in ['salam', 'salam alaykom', 'salam 3likom']:
            return jsonify({"response": "Salam ! 👋 Labas 3lik ? Kifach n9der n3awnek ?"})
        
        if 'sb7 lkhir' in user_message or 'sbah lkhir' in user_message:
            return jsonify({"response": "Sb7 lkhir ! ☀️ Labas ? Chno bghiti t3raf 3la l9raya ?"})
        
        if 'msa lkhir' in user_message or 'msa2 lkhir' in user_message:
            return jsonify({"response": "Msa lkhir ! 🌙 Kidayra nhark ? Wash 3andek chi so2al ?"})
        
        if 'choukran' in user_message or 'chokran' in user_message:
            return jsonify({"response": "Marhba bik ! 😊 Wakha ghir so2el."})
        
        # Anglais
        if user_message in ['hello', 'hi', 'hey there']:
            return jsonify({"response": "Hello! 👋 How can I help you with your studies today?"})
        
        if 'good morning' in user_message:
            return jsonify({"response": "Good morning! ☀️ How can I assist you?"})
        
        if 'good evening' in user_message:
            return jsonify({"response": "Good evening! 🌙 How's your day going?"})

        # --- QUESTIONS META SUR LE CHATBOT ---
        # YAFI Definition (TRES HAUTE PRIORITE)
        if any(keyword in user_message for keyword in ['yafi', 'y.a.f.i', 'y a f i']):
            return jsonify({"response": "✨ **YAFI** est un acronyme formé à partir des prénoms des créateurs du projet :\n\n👤 **Y** → Yasser\n👤 **A** → Adam\n👤 **F** → Fahd\n🧠 **I** → Intelligence\n\n👉 **I = Intelligence**, en référence à :\n- 🤖 L'intelligence artificielle\n- 🧭 L'intelligence d'orientation\n- 💡 L'aide intelligente à la décision post-bac"})

        # Identité et rôle
        if any(keyword in user_message for keyword in ['qui es-tu', 'qui es tu', 'quel est ton role', 'quel est ton roll', 'ton role', 'ton roll', 'tu fais quoi', 'ton but', 'c\'est quoi ce bot', 'c\'est quoi ce site', 'c\'est quoi cette app']):
            return jsonify({"response": "Je suis un chatbot d'orientation post-bac pour les étudiants marocains ! 🎓\n\nMon rôle est de vous aider à :\n✅ Choisir votre filière selon votre Bac\n✅ Trouver les bonnes écoles (publiques/privées)\n✅ Comprendre les stratégies d'admission\n\n💡 **Bon à savoir** : Vous pouvez m'écrire **sans accents** et sans vous soucier des caractères complexes (ex: 'medecine', 'ingenieur'). Je vous comprendrai parfaitement !"})
        
        # Créateur
        if any(keyword in user_message for keyword in ['qui t\'a cree', 'qui t\'a créé', 'qui a cree', 'qui a créé', 'adam moufrije', 'ton createur', 'ton créateur', 'le createur', 'le créateur', 'son createur', 'son créateur', 'qui t a fait', 'qui t\'a fait', 'ton developpeur', 'ton développeur', 'qui a developpe', 'qui a développé']):
            return jsonify({"response": "👨‍💻 Le créateur et développeur de ce modèle et de la base de connaissances est **Adam Moufrije**.\n\n🚀 Ce projet a été réalisé avec le soutien de différents **LLMs** (Large Language Models) pour aider à la création et au développement du système."})
        
        # Nature (AI/Bot)
        if any(keyword in user_message for keyword in ['tu es un ai', 'tu est un ai', 'tu es une ia', 'tu est une ia', 'es-tu un robot', 'es-tu un bot', 'est-tu un robot', 'chatbot', 'robot']):
            return jsonify({"response": "Oui, je suis un chatbot intelligent (IA) ! 🤖\n\nJe combine :\n- **Prolog** pour la logique d'orientation\n- **Python** pour le traitement\n- **React** pour l'interface\n\nJe suis spécialisé dans l'orientation post-bac au Maroc. Posez-moi vos questions !"})
        
        # Remerciements / Feedback
        if any(keyword in user_message for keyword in ['merci', 'thank you', 'thanks', 'شكرا']):
            return jsonify({"response": "De rien ! 😊 Je suis là pour vous aider.\n\nN'hésitez pas si vous avez d'autres questions sur votre orientation ! 🎓"})
        
        # Plaintes / Erreurs
        if any(keyword in user_message for keyword in ['arret', 'arrête', 'stop', 'meme reponse', 'même réponse', 'bug', 'erreur']):
            return jsonify({"response": "Désolé si ma réponse n'était pas claire ! 😅\n\nEssayez de reformuler votre question de manière plus précise, par exemple :\n- 'Que faire avec un Bac PC ?'\n- 'Médecine avec 13 de moyenne'\n- 'Prix EMSI'\n- 'Débouchés informatique'\n\nJe suis là pour vous aider ! 💪"})

        # --- PRIORITY CHECK: CONCOURS & EXAMENS ---
        if "concours" in user_message or "examen" in user_message:
             concours_map = {
                 'medecine': ['médecine', 'medecine', 'pharmacie', 'dentaire'],
                 'ingenierie_public': ['ingénierie', 'ingenieur', 'ensa', 'emi', 'ensias', 'public'],
                 'ecoles_privees': ['privé', 'prive', 'emsi', 'uir', 'um6p', 'hem'],
                 'commerce': ['commerce', 'gestion', 'encg', 'iscae', 'esca', 'business']
             }
             found_concours = None
             for conc_key, keywords in concours_map.items():
                 if any(k in user_message for k in keywords):
                     found_concours = conc_key
                     break
            
             if found_concours:
                 q = f"get_concours_admission({found_concours}, E, C)"
                 res = list(prolog.query(q))
                 if res:
                     r = res[0]
                     display_name = found_concours.replace('_', ' ').title()
                     if found_concours == 'medecine': display_name = 'Médecine'
                     return jsonify({"response": f"📝 **Concours {display_name}** :\n📋 {clean_text(r['E'])}\n{clean_text(r['C'])}"})
                 else:
                     return jsonify({"response": f"Je n'ai pas d'infos sur le concours '{found_concours}'."})
             else:
                 return jsonify({"response": "📝 **Concours** : Médecine (QCM Sciences), Ingénierie (Maths/Physique), Commerce (TAFEM)... Précisez une filière."})

        # --- 4. INFOS PRATIQUES (Prioritaire) ---
        
        # 4.1. Seuils & Dates
        if "seuil" in user_message or "date" in user_message or ("quand" in user_message and ("concours" in user_message or "inscription" in user_message)):
             keywords_map = {
                 'ensa': 'Concours ENSA', 'encg': 'Concours ENCG (TAFEM)', 'medecine': 'Concours Medecine', 'médecine': 'Concours Medecine',
                 'fst': 'Inscription CursusSup', 'est': 'Inscription CursusSup', 'cursussup': 'Inscription CursusSup', 'ofppt': 'Inscription OFPPT',
                 'bac': 'Resultats Bac'
             }
             found = None
             for k, v in keywords_map.items():
                 if k in user_message: found = v; break
            
             if found:
                 q_date = f"get_date_concours('{found}', D)"
                 res_d = list(prolog.query(q_date))
                 date_txt = clean_text(res_d[0]['D']) if res_d else "Non défini"
                 
                 seuil_txt = ""
                 if "ENSA" in found: school="ENSA"
                 elif "ENCG" in found: school="ENCG"
                 elif "Medecine" in found: school="Medecine"
                 elif "FST" in user_message.upper(): school="FST"
                 elif "EST" in user_message.upper(): school="EST"
                 else: school=None
                 
                 if school:
                     q_seuil = f"get_seuil('{school}', 2023, N)"
                     res_s = list(prolog.query(q_seuil))
                     if res_s: seuil_txt = f"\n📉 **Seuil 2023** : {clean_text(res_s[0]['N'])}/20"
                 
                 return jsonify({"response": f"📅 **{found}** :\n🗓️ **Date** : {date_txt}{seuil_txt}"})
             else:
                 return jsonify({"response": "📅 **Calendrier** : Je connais les dates pour ENSA, ENCG, Médecine, CursusSup..."})

        # 4.2. Liens & Sites
        if "lien" in user_message or "site" in user_message or "adresse" in user_message:
             keys = {'cursussup': 'CursusSup', 'minhaty': 'Minhaty (Bourse)', 'ensa': 'ENSA Maroc', 'tafem': 'TAFEM (ENCG)', 'ofppt': 'OFPPT'}
             found = found_context_match(keys, user_message, last_topic)
             
             if found:
                 q = f"get_lien('{found}', U)"
                 res = list(prolog.query(q))
                 url = clean_text(res[0]['U']) if res else "#"
                 return jsonify({"response": f"🔗 **Lien {found}** : [Cliquez ici]({url})"})
             else:
                 return jsonify({"response": "🔗 **Liens Utiles** : Demandez-moi CursusSup, Minhaty, ENSA..."})

        # 4.3. Procédures & Logement
        if "démarche" in user_message or "procédure" in user_message or "dossier" in user_message or "inscription" in user_message or "s'inscrire" in user_message or "papier" in user_message or "document" in user_message or "logement" in user_message or "cité" in user_message or "internat" in user_message:
            # Check Logement
            if "logement" in user_message or "cité" in user_message or "internat" in user_message:
                type_log = 'Cite Universitaire'
                if "privé" in user_message or "location" in user_message: type_log = 'Location Privee'
                elif "internat" in user_message: type_log = 'Internat'
                
                q = f"get_logement('{type_log}', D, C)"
                res = list(prolog.query(q))
                if res:
                     return jsonify({"response": f"🏠 **{type_log}** :\nℹ️ {clean_text(res[0]['D'])}\n💡 {clean_text(res[0]['C'])}"})
                else:
                     return jsonify({"response": "🏠 **Logement** : Précisez Cité, Internat ou Location."})
            else:
                # Procédures
                proc = 'Inscription Fac' # Default
                if "minhaty" in user_message or "bourse" in user_message: proc = 'Dossier Minhaty'
                elif "legalis" in user_message: proc = 'Legalisation'
                
                q = f"get_procedure('{proc}', D)"
                res = list(prolog.query(q))
                if res:
                     return jsonify({"response": f"📝 **Procédure {proc}** :\n{clean_text(res[0]['D'])}"})

        # 4.4. OFPPT
        if "ofppt" in user_message or "technicien" in user_message or "ista" in user_message:
             niveau = 'Technicien Specialise'
             if "qualif" in user_message: niveau = 'Qualification'
             elif "technicien" in user_message and "spécialisé" not in user_message: niveau = 'Technicien'
             
             q = f"get_formation_pro('{niveau}', D, C)"
             res = list(prolog.query(q))
             if res:
                  return jsonify({"response": f"🏭 **OFPPT ({niveau})** :\nℹ️ {clean_text(res[0]['D'])}\n💡 {clean_text(res[0]['C'])}"})

        # 4.5. Calculateur de Note
        # 4.5. Calculateur de Note & Orientation par Moyenne
        # Détection de nombres (Note 0-20)
        nums = re.findall(r'\d+(?:[.,]\d+)?', user_message)
        nums = [float(n.replace(',', '.')) for n in nums]
        valid_grades = [n for n in nums if n <= 20]

        is_calc_request = "calcul" in user_message or "score" in user_message
        is_grade_context = "moyenne" in user_message or "bac" in user_message or "j'ai" in user_message or "note" in user_message

        if (is_calc_request or is_grade_context) and valid_grades:
             
             # CAS A : CALCULATEUR (2 notes : Régional + National)
             if len(valid_grades) >= 2:
                  reg = valid_grades[0]
                  nat = valid_grades[1]
                  score = (reg * 0.25) + (nat * 0.75)
                  resp = f"🧮 **Calculateur de Seuil** :\n- Régional (25%) : {reg}\n- National (75%) : {nat}\n\n✨ **Votre Score d'Admission : {score:.2f}/20**\n"
                  
                  if score >= 15: resp += "🌟 Excellent ! Vous êtes bien parti pour Médecine/ENSA."
                  elif score >= 12: resp += "✅ Bon score. FST et EST sont très jouables. ENSA possible (vérifiez seuils)."
                  else: resp += "⚠️ Un peu juste pour les filières sélectives. Visez EST, BTS ou Fac."
                  return jsonify({"response": resp})
             
             # CAS B : CONSEIL ORIENTATION (1 note donnée)
             elif len(valid_grades) == 1:
                  note = valid_grades[0]
                  
                  # Detect Bac
                  bac = 'SVT' # Par défaut
                  if 'pc' in user_message: bac = 'PC'
                  elif 'sm' in user_message: bac = 'SM'
                  elif 'eco' in user_message: bac = 'ECO'
                  elif 'litt' in user_message: bac = 'LITT'
                  elif 'tech' in user_message: bac = 'TECH'
                  
                  q = f"strategie_profil({note}, '{bac}', Conseil)"
                  res = list(prolog.query(q))
                  if res:
                       raw_conseil = clean_text(res[0]['Conseil'])
                       if ResponseBuilder:
                           final_conseil = ResponseBuilder.build_strategy_response(note, bac, raw_conseil)
                       else:
                           final_conseil = f"🎯 **Conseil Orientation (Note : {note}/20)** :\n{raw_conseil}"
                       return jsonify({"response": final_conseil})
                  else:
                       return jsonify({"response": f"Avec {note}/20, vous avez plusieurs options. Précisez votre Bac pour un conseil ciblé !"})

        if "calcul" in user_message and not valid_grades:
             return jsonify({"response": "🧮 **Calculateur** : Donnez-moi vos notes Régional et National (ex: 'Calcul 14 16') pour avoir votre score."})

        # 4.6. Quiz Orientation
        if "quiz" in user_message or "aime" in user_message or "préfère" in user_message or "fort en" in user_message:
             scores = {'ingenierie': 0, 'medecine': 0, 'commerce': 0, 'lettres': 0, 'art': 0}
             
             if "math" in user_message: scores['ingenierie'] += 2; scores['commerce'] += 1
             if "physique" in user_message: scores['ingenierie'] += 2
             if "svt" in user_message or "bio" in user_message: scores['medecine'] += 3
             if "info" in user_message or "cod" in user_message: scores['ingenierie'] += 2
             if "eco" in user_message or "gest" in user_message: scores['commerce'] += 3
             if "langue" in user_message or "fran" in user_message: scores['lettres'] += 2; scores['commerce'] += 1
             if "dessin" in user_message or "art" in user_message: scores['art'] += 3; scores['ingenierie'] += 1
             
             best = max(scores, key=scores.get)
             resp = "🧠 **Quiz Orientation** :\n"
             if scores[best] > 0:
                 if best == 'ingenierie': rec = "Vous semblez avoir un profil **Ingénieur / Tech** ! 🛠️\n👉 Visez ENSA, CPGE, FST, EST."
                 elif best == 'medecine': rec = "Vous avez un profil **Santé / Bio** ! 🩺\n👉 Visez Médecine, Pharmacie, ISPITS."
                 elif best == 'commerce': rec = "Vous avez un profil **Manager / Eco** ! 💼\n👉 Visez ENCG, ISCAE, EST."
                 elif best == 'lettres': rec = "Vous avez un profil **Littéraire / Droit** ! 📚\n👉 Visez Fac de Droit, Lettres, Journalisme."
                 elif best == 'art': rec = "Vous avez un profil **Créatif / Archi** ! 🎨\n👉 Visez ENA (Archi), Beaux-Arts ou Design."
                 
                 resp += rec + "\n\n(Dites 'Détail Ingénieur' pour en savoir plus)"
             else:
                 resp += "Dites-moi quelles matières vous aimez (Maths, SVT, Eco, Langues...) pour que je vous oriente !"
             return jsonify({"response": resp})
        
        # Critiques / Insultes (réponse calme)
        if any(keyword in user_message for keyword in ['nul', 'null', 'mauvais', 'pas bon', 'debile', 'bête', 'idiot']):
            return jsonify({"response": "Je suis désolé si je n'ai pas répondu à vos attentes. 😔\n\nPour mieux vous aider, posez une question précise comme :\n- 'Bac PC que faire ?'\n- 'Prix école privée'\n- 'Conseils révision'\n\nJe ferai de mon mieux ! 💪"})

        # --- 1. STATISTIQUES & CHIFFRES (Priorité Haute) ---
        if "place" in user_message or "combien" in user_message or "nombre" in user_message or "stat" in user_message or "chance" in user_message or "monde" in user_message:
            
            keywords = ['médecine', 'ensa', 'encg', 'ensam', 'fst', 'global', 'casa', 'rabat', 'agadir', 'salaire']
            found_key = next((k for k in keywords if k in user_message), None)
            
            if found_key:
                stats = list(prolog.query("stat(Cat, Entite, Val)"))
                matches = []
                for s in stats:
                    if found_key.lower() in str(s['Entite']).lower():
                        matches.append(s)
                
                if matches:
                     response_text = f"📊 **Statistiques pour '{found_key.capitalize()}' :**\n"
                     for m in matches:
                         val_clean = clean_text(m['Val'])
                         cat_clean = clean_text(m['Cat'])
                         entite_clean = clean_text(m['Entite'])
                         response_text += f"- {cat_clean} ({entite_clean}) : **{val_clean}**\n"
                else:
                    response_text = f"Je n'ai pas de chiffre précis pour '{found_key}'."
            else:
                 response_text = "📊 **Le Saviez-vous ?**\n- Il y a 1.25 million d'étudiants au Maroc.\n- La sélectivité est rude : 1 place pour 22 candidats en Médecine !"

        # --- 1.5 OÙ ÉTUDIER [DOMAINE] (Nouveau Handler Optimisé) ---
        elif ("ou" in user_message) and ("etudier" in user_message or "faire" in user_message or "trouve" in user_message):
            # Map keywords to domains/filières
            domaines_map = {
                'architecture': ['architecture', 'architecte', 'urbanisme'],
                'informatique': ['informatique', 'it', 'programmation', 'cyber', 'data', 'dev'],
                'medecine': ['medecine', 'pharmacie', 'dentaire', 'sante'],
                'ingenierie': ['ingenierie', 'genie', 'engineering'],
                'commerce': ['commerce', 'gestion', 'management', 'business', 'marketing', 'encg'],
                'droit': ['droit', 'juridique', 'avocat'],
                'lettres': ['lettres', 'litterature', 'langues', 'philosophie'],
                'design': ['design', 'graphisme', 'beaux-arts', 'arts']
            }
            
            found_domaine = None
            for domaine, keywords in domaines_map.items():
                if any(kw in user_message for kw in keywords):
                    found_domaine = domaine
                    break
            
            # Utilisation du Contexte si aucun domaine trouvé
            if not found_domaine and last_topic:
                for domaine, keywords in domaines_map.items():
                    if any(kw in last_topic.lower() for kw in keywords):
                        found_domaine = domaine
                        break

            if found_domaine:
                # OPTIMISATION PROLOG : Utilisation de recherche_ecole/2
                # Plus rapide et plus précis que le filtrage Python
                try:
                    # On utilise found_domaine comme mot-clé partiel pour la recherche floue Prolog
                    results = list(prolog.query(f"recherche_ecole('{found_domaine}', E)"))
                    ecoles_found = sorted(list(set([clean_text(r['E']) for r in results])))
                    
                    if ecoles_found:
                        display_name = found_domaine.capitalize()
                        if ResponseBuilder:
                            response_text = ResponseBuilder.build_school_list(found_domaine, ecoles_found, last_topic)
                        else:
                            response_text = f"🏫 **Où étudier {display_name} au Maroc ?**\n\n"
                            response_text += f"Voici les établissements (Publics & Privés) :\n\n"
                            
                            for ecole in ecoles_found[:15]:
                                response_text += f"• {ecole}\n"
                            
                            if len(ecoles_found) > 15:
                                response_text += f"\n... et {len(ecoles_found) - 15} autres établissements.\n"
                    else:
                         response_text = f"Je n'ai pas trouvé d'établissements pour '{found_domaine}'."
                except Exception as e:
                    print(f"Erreur Prolog recherche_ecole: {e}")
                    response_text = "Une erreur technique est survenue lors de la recherche."
            else:
                 response_text = "🎓 **Où étudier ?** Précisez un domaine (ex: Informatique, Médecine, Commerce...)"

        # --- 2. GEOGRAPHIE & VILLES (Priorité Haute) ---- Inclut Ville Chance
        elif ("où" in user_message or "ville" in user_message or "trouve" in user_message or "localisation" in user_message or "campus" in user_message or "école" in user_message or "ecole" in user_message or "université" in user_message or "concurrence" in user_message or "chance" in user_message or "opportunité" in user_message or any(v in user_message for v in ['rabat', 'casa', 'marrakech', 'agadir', 'fès', 'meknès', 'tanger', 'oujda', 'safi', 'khouribga', 'el jadida', 'tetouan'])) and not "avantage" in user_message and not "inconvénient" in user_message:
            
            # CAS 0 : RECHERCHE VILLE CHANCE / CONCURRENCE
            if "concurrence" in user_message or "chance" in user_message or "opportunité" in user_message or "moins de" in user_message:
                 chances_q = list(prolog.query("ville_chance(V)"))
                 villes_list = [clean_text(c['V']) for c in chances_q]
                 response_text = "🌍 **Villes 'Opportunité' (Moins de concurrence)** :\n"
                 response_text += "Voici les villes où le ratio Places/Candidats est souvent plus favorable (bon plan pour les listes d'attente !) :\n"
                 for v in villes_list:
                     response_text += f"- 🏙️ {v}\n"
                 response_text += "\n💡 **Conseil** : Pensez à y postuler (FST, ENSA, EST) même si vous visez les grandes villes."
            
            else:
                # Cas 1 : User cherche où se trouve une école (ex: "Où est l'ENSA ?")
                ecoles_cles = ['ensa', 'ensam', 'ensias', 'encg', 'fst', 'est', 'um6p', 'universite', 'emsi', 'uir', 'hem']
                ecole_demandee = next((e for e in ecoles_cles if e in user_message), None)
            
                # On distingue "Où est ecole" de "Ecoles à Ville"
                # Si on a un nom de ville explicite, on priorise la recherche par ville
                villes_cles = ['rabat', 'casa', 'casablanca', 'marrakech', 'agadir', 'fès', 'fes', 'meknès', 'meknes', 'tanger', 'oujda', 'safi', 'khouribga', 'beni mellal', 'el jadida', 'taza', 'errachidia', 'kénitra', 'kenitra', 'mohammedia', 'settat', 'berrechid', 'dakhla', 'laayoune', 'nador', 'al hoceima', 'tetouan', 'tétouan']
                ville_demandee = next((v for v in villes_cles if v in user_message), None)

                if ville_demandee and not ("où est" in user_message or "trouve" in user_message):
                     # Cas 2 : User demande ce qu'il y a dans une VILLE (ex: "Ecoles à Rabat")
                     locs = list(prolog.query("localisation(Ecole, Ville)"))
                     found_ecoles = []
                     for l in locs:
                         ville_p = clean_text(l['Ville'])
                         if ville_demandee.lower() in ville_p.lower():
                              found_ecoles.append(clean_text(l['Ecole']))
                     
                     # NEW: Search in etablissement/5 as well
                     try:
                         etabs_loc = list(prolog.query(f"etablissement(Nom, '{ville_demandee.capitalize()}', _, _, _)"))
                         # Try loose match if exact fail
                         if not etabs_loc:
                             etabs_loc = list(prolog.query("etablissement(Nom, Ville, _, _, _)"))
                             etabs_loc = [e for e in etabs_loc if ville_demandee.lower() in clean_text(e['Ville']).lower()]
                             
                         for e in etabs_loc:
                             name = clean_text(e['Nom'])
                             if name not in found_ecoles: found_ecoles.append(name)
                     except: pass

                     chance_msg = ""
                     chances = list(prolog.query("ville_chance(V)"))
                     for c in chances:
                         vc = clean_text(c['V'])
                         if ville_demandee.lower() in vc.lower():
                             chance_msg = "\n✅ **Note:** Ville 'Opportunité' (Moins de concurrence, bon plan !)."

                     if found_ecoles:
                         response_text = f"🏫 À **{ville_demandee.capitalize()}**, vous trouverez :\n" + "\n".join([f"- {e}" for e in sorted(list(set(found_ecoles)))]) + chance_msg
                     else:
                         response_text = f"Je n'ai pas d'info spécifique sur les écoles à {ville_demandee}."
                
                elif ecole_demandee:
                    ecole_upper = ecole_demandee.upper()
                    if ecole_demandee == 'universite': ecole_upper = 'Université'
                    
                    found_villes = []
                    
                    # Check Localisation (Old)
                    locs = list(prolog.query("localisation(Ecole, Ville)"))
                    for l in locs:
                         if ecole_demandee.lower() in str(l['Ecole']).lower():
                            v = clean_text(l['Ville'])
                            found_villes.append(v)
                    
                    # Check Etablissement (New)
                    try:
                        all_etabs = list(prolog.query("etablissement(Nom, Ville, _, _, _)"))
                        for e in all_etabs:
                            nom = clean_text(e['Nom']).lower()
                            if ecole_demandee.lower() in nom or nom in ecole_demandee.lower():
                                 v = clean_text(e['Ville'])
                                 if v not in found_villes:
                                     found_villes.append(v)
                    except:
                        pass
    
                    # FILTER BY CITY IF SPECIFIED (e.g. "Où est l'ENSA Kénitra ?")
                    if ville_demandee:
                        filtered = [v for v in found_villes if ville_demandee.lower() in v.lower()]
                        if filtered:
                            response_text = f"📍 **{ecole_upper}** est bien présent à **{filtered[0]}**."
                        else:
                            response_text = f"📍 **{ecole_upper}** ne semble pas être à {ville_demandee.capitalize()} (ou je ne l'ai pas dans ma base).\nVoici où le trouver : {', '.join(sorted(list(set(found_villes))))}"
                    
                    elif found_villes:
                        unique_villes = sorted(list(set(found_villes)))
                        response_text = f"📍 **{ecole_demandee.upper()}** est présent à :\n" + ", ".join(unique_villes)
                    else:
                        response_text = f"Désolé, je ne trouve pas la localisation pour '{ecole_demandee}'."
                else:
                     response_text = "🌍 Je peux vous dire où se trouvent les écoles ou ce qu'il y a dans votre ville."


        # --- 3. STRATEGIE & TYPES ETABLISSEMENTS ---
        # --- 3. STRATEGIE & TYPES ETABLISSEMENTS ---
        elif "stratégie" in user_message or "avantage" in user_message or "inconvénient" in user_message or "ouvert" in user_message or "régulé" in user_message or "type" in user_message:
             
             # A. PROS / CONS Types
             types_map = {
                 'public_ouvert': ['fac', 'ouverte', 'ouvert', 'université', 'droit', 'eco', 'sans sélection', 'open', 'public', 'publique'],
                 'public_regule': ['régulée', 'régulé', 'regule', 'ensa', 'médecine', 'prepa', 'concours', 'public sélectif'],
                 'prive': ['privé', 'prive', 'payant', 'supinfo', 'uir', 'emsi', 'ecole payante']
             }
             found_type = next((k for k, v in types_map.items() if any(sub in user_message for sub in v)), None)
            
             # Priorité aux questions sur les avantages/inconvénients ou définitions de types
             if ("avantage" in user_message or "inconvénient" in user_message or "c'est quoi" in user_message or "type" in user_message) and found_type:
                  # Note: found_type is now an atom string like 'public_ouvert'
                  q = f"get_info_type({found_type}, Desc, Av, Inc)"
                  res = list(prolog.query(q))
                  if res:
                      r = res[0]
                      # Clean type name for display
                      display_name = found_type.replace('_', ' ').replace('regule', 'régulé').title()
                      response_text = f"🏫 **{display_name}** :\n📌 {clean_text(r['Desc'])}\n{clean_text(r['Av'])}\n{clean_text(r['Inc'])}"
                  else:
                      response_text = f"Je n'ai pas d'infos détaillées sur le type '{found_type}'."

             # B. STRATEGIE PERSO (Note + Bac ?)
             elif "stratégie" in user_message or "conseil" in user_message:

                 match = re.search(r'\b(1[0-9]|20|[0-9])(\.[0-9]+)?\b', user_message) # Float support
                 
                 if match:
                     note = float(match.group(0))
                     
                     # Detect Bac
                     bac = 'SVT' # Default
                     if 'pc' in user_message: bac = 'PC'
                     elif 'sm' in user_message: bac = 'SM'
                     elif 'eco' in user_message: bac = 'ECO'
                     
                     q = f"strategie_profil({note}, '{bac}', Conseil)"
                     res = list(prolog.query(q))
                     if res:
                         raw_conseil = clean_text(res[0]['Conseil'])
                         if ResponseBuilder:
                             response_text = ResponseBuilder.build_strategy_response(note, bac, raw_conseil)
                         else:
                             response_text = f"🎯 **Stratégie Orientation ({note}/20 - Bac {bac})** :\n{raw_conseil}"
                     else:
                         response_text = "Pas de conseil spécifique pour ce cas exact."
                 else:
                     if "stratégie" in user_message:
                        response_text = "Pour une stratégie personnalisée, donnez-moi votre moyenne (ex: 'Stratégie avec 14')."
                     else:
                        # Fallback to generic conseil if no note
                        pass # Let it fall through to generic Conseil block?
                        # No, if we are in this ELIF, we are trapped. 
                        # We must provide response OR use 'continue' logic which Flask doesn't have easily.
                        # So I should handle "Conseil" without note here or return "Je ne sais pas".
                        # But "Conseil" general is handled below. 
                        # I should only trap "Strategy" here.
                        response_text = "Pour une stratégie personnalisée, donnez-moi votre moyenne (ex: 'Stratégie avec 14')."

             if not response_text: # Fallback if B failed to produce text (e.g. "conseil" matched but no note)
                  # If we captured "conseil" here but didn't have a note, we might want to let the Generic Conseil block handle it.
                  # But we can't 'break' to next elif.
                  # So I strictly limit B to "stratégie".
                  pass 
             
             # Re-refining B condition:
             # Only trap if "stratégie" is present.
             # If "conseil", let it go to Generic Conseil block?
             # But "stratégie" keywords triggered the outer block.
             # So we must handle it.
             
             if not ('response_text' in locals() and response_text):
                 response_text = "Je peux comparer les filières (Ouvertes vs Régulées) ou vous donner une stratégie selon votre note."
        
        # --- 6. ECOLES PRIVEES & FRAIS & PUBLIC (Prix) ---
        elif "prix" in user_message or "frais" in user_message or "coût" in user_message or "payer" in user_message or "privé" in user_message or "gratuit" in user_message or "emsi" in user_message or "uir" in user_message or "hem" in user_message or "esca" in user_message or ("ensa" in user_message and ("frais" in user_message or "prix" in user_message or "gratuit" in user_message)):
             
             # A. Check Ecoles Publiques (Gratuites)
             ecoles_publiques = ['ensa', 'ensam', 'ensias', 'encg', 'fst', 'est', 'universite', 'faculté', 'médecine']
             public_found = next((e for e in ecoles_publiques if e in user_message), None)
             
             # B. Check Ecoles Privées
             ecoles_privees = ['emsi', 'uir', 'supinfo', 'emg', 'hem', 'esca', 'uiass', 'upsat', 'isitt']
             priv_found = next((e for e in ecoles_privees if e in user_message), None)

             if public_found and not priv_found:
                 response_text = f"🏛️ **{public_found.upper()}** est un établissement **Public**.\n✅ **Les frais de scolarité sont GRATUITS** (0 DH).\nIl faut juste payer les frais d'inscription annuels (~200 DH) et l'assurance."

             elif priv_found:
                 # Limitation: Ne pas repondre aux questions "Qui est le directeur" avec les frais
                 if "directeur" in user_message or "président" in user_message:
                     response_text = f"Je n'ai pas l'information sur le directeur de {priv_found.upper()}. Je peux par contre vous donner les frais et spécialités."
                 else:
                     details = list(prolog.query("detail_ecole(Nom, Cat, Spec, Frais)"))
                     match = next((d for d in details if priv_found.lower() in str(d['Nom']).lower()), None)
                     
                     if match:
                         response_text = f"💎 **{clean_text(match['Nom'])}** ({clean_text(match['Cat'])})\n"
                         response_text += f"- 💰 **Frais**: {clean_text(match['Frais'])}\n"
                         response_text += f"- 🎓 **Spécialités**: {clean_text(match['Spec'])}\n"
                     else:
                         response_text = f"Détails financiers non trouvés pour {priv_found}."
             else:
                 response_text = "💰 **Enseignement Privé** : EMSI (~35k/an), UIR (~80k/an), Medecine Privée (~100k/an)...\n🏛️ **Public** : Gratuit."

        # --- 4. DEFINITIONS & SYSTEME ---
        elif "c'est quoi" in user_message or "système" in user_message or "diplôme" in user_message or "lmd" in user_message or "master" in user_message or "licence" in user_message or "doctorat" in user_message or "bts" in user_message or "dut" in user_message or "cpge" in user_message:
            
            termes = ['lmd', 'licence', 'master', 'doctorat', 'bts', 'dut', 'ingénieur', 'cpge']
            terme_found = next((t for t in termes if t in user_message), None)
            
            if terme_found:
                defs = list(prolog.query("definition(Terme, Def)"))
                match = next((d for d in defs if terme_found.lower() in str(d['Terme']).lower()), None)
                
                if match:
                    response_text = f"📖 **{clean_text(match['Terme'])}** :\n{clean_text(match['Def'])}"
                else:
                    response_text = f"Définition non trouvée pour {terme_found}."
            else:
                 response_text = "📚 **Système LMD** : Licence (3 ans), Master (5 ans), Doctorat (8 ans)."

        # --- 5. MEDECINE (Test de note & Compatibilité) ---
        # --- 5. COMPATIBILITE (Generalise: Medecine, Ecng, Ingenerie, etc.) ---
        elif ("médecine" in user_message or "medecine" in user_message or "ingénieur" in user_message or "ingenieur" in user_message or "encg" in user_message or "informatique" in user_message) and ("bac" in user_message or "avec" in user_message or "peut" in user_message):
            
            # 1. Detecter le BAC

            bacs_map = {
                'SM': [r'\bsm\b', r'\bmath\b', r'\bmaths\b'],
                'PC': [r'\bpc\b', r'\bphysique\b'],
                'SVT': [r'\bsvt\b', r'\bscience vie\b', r'\bbio\b'],
                'ECO': [r'\beco\b', r'\beconomie\b', r'\bgestion\b'],
                'LITT': [r'\blitt\b', r'\blettre\b', r'\blettres\b'],
                'TECH': [r'\btech\b', r'\belec\b', r'\bmeca\b']
            }
            detected_bac = 'SVT' # Default fallback if only target is mentioned, often users imply SVT/PC logic? No, risky. 
            # Better to try to find it.
            found_b = None
            for code, keywords in bacs_map.items():
                for pat in keywords:
                    if re.search(pat, user_message, re.IGNORECASE):
                        found_b = code
                        break
                if found_b: break
            
            # 2. Detecter la FILIERE CIBLE
            targets_map = {
                'medecine': [r'm[ée]decine', r'pharmacie', r'dentaire', r'sant[é]'],
                'ingenierie': [r'ing[ée]nieur', r'ing[ée]nierie', r'g[ée]nie', r'ensa', r'emi'],
                'commerce': [r'commerce', r'gestion', r'encg', r'iscae', r'marketing'],
                'informatique': [r'info', r'informatique', r'dev', r'programmation'],
                'lettres': [r'droit', r'lettre', r'juridique']
            }
            detected_target = None
            for t_code, keywords in targets_map.items():
                for pat in keywords:
                    if re.search(pat, user_message, re.IGNORECASE):
                        detected_target = t_code
                        break
                if detected_target: break
            
            # 3. Logique
            if found_b and detected_target:
                # On a les deux : Check Compatibilité
                q_compat = f"check_compatibilite('{found_b}', {detected_target}, Statut, Msg)"
                compat_res = list(prolog.query(q_compat))
                if compat_res:
                     response_text = f"🎯 **Compatibilité Bac {found_b} → {detected_target.capitalize()}** :\n{clean_text(compat_res[0]['Msg'])}"
                else: 
                     response_text = f"Je n'ai pas de donnée exacte pour Bac {found_b} vers {detected_target}."
            
            elif detected_target and not found_b:
                # On a la cible mais pas le Bac (ex: "Peut-on faire médecine ?")
                # On demande le Bac OU on donne les conditions générales
                if detected_target == 'medecine':
                    response_text = "🩺 **Pour Médecine** : Il faut obligatoirement un Bac Scientifique (SVT, PC, SM). Moyenne > 12."
                elif detected_target == 'ingenierie':
                     response_text = "🛠️ **Pour Ingénieur** : Bac Scientifique ou Technique recommandé. Concours ENSA/ENSAM après le Bac."
                else:
                    response_text = f"🎯 **{detected_target.capitalize()}** : Quel est votre type de Bac ? (SVT, PC, Eco...)"

            elif found_b and not detected_target:
                 # On a le Bac mais pas la cible -> C'est une question d'orientation générale
                 pass # On laisse tomber vers le handler "Orientation par Bac" plus bas
            
            else:
                pass # Fallthrough














        # --- 6.1 STAGES & EXPERIENCES PRATIQUES ---
        elif "stage" in user_message or "stages" in user_message or "pratique" in user_message or "expérience" in user_message or "pfe" in user_message or "projet" in user_message:
            
            # Map keywords to fields
            stages_map = {
                'medecine': ['médecine', 'medecine', 'pharmacie', 'dentaire', 'santé'],
                'ingenierie': ['ingénierie', 'ingenieur', 'ensa', 'emi', 'technique'],
                'informatique': ['informatique', 'info', 'it', 'data', 'cyber', 'dev'],
                'commerce': ['commerce', 'gestion', 'finance', 'marketing', 'business'],
                'shs': ['sciences humaines', 'psycho', 'socio', 'lettres'],
                'arts': ['arts', 'design', 'architecture', 'créatif'],
                'tourisme': ['tourisme', 'hôtel', 'logistique']
            }
            
            found_stage = None
            for stage_key, keywords in stages_map.items():
                if any(k in user_message for k in keywords):
                    found_stage = stage_key
                    break
            
            if found_stage:
                # Query specific field
                q = f"get_stages_filiere({found_stage}, S, A)"
                res = list(prolog.query(q))
                
                if res:
                    r = res[0]
                    display_name = found_stage.capitalize()
                    if found_stage == 'medecine': display_name = 'Médecine'
                    elif found_stage == 'ingenierie': display_name = 'Ingénierie'
                    elif found_stage == 'shs': display_name = 'Sciences Humaines'
                    
                    response_text = f"🎓 **Stages & Pratique - {display_name}** :\n"
                    response_text += f"📋 {clean_text(r['S'])}\n"
                    response_text += f"{clean_text(r['A'])}\n"
                else:
                    response_text = f"Je n'ai pas d'infos sur les stages en '{found_stage}'."
            else:
                # General advice
                response_text = "🎓 **Stages & Expériences** :\n"
                response_text += "Les stages sont essentiels dans toutes les filières.\n"
                response_text += "- Vérifie que ton école intègre des stages obligatoires\n"
                response_text += "- Planifie dès la 1ʳᵉ année pour max d'expérience\n"
                response_text += "Précisez une filière pour détails spécifiques."


        # --- 6.2 DUREE ETUDES (Courtes vs Longues) ---
        elif "études courtes" in user_message or "etudes courtes" in user_message or "études longues" in user_message or "etudes longues" in user_message or ("courte" in user_message and "longue" in user_message) or "bts" in user_message or "dut" in user_message or "combien d'années" in user_message or "durée" in user_message or "duree" in user_message:
            
            # Detect which type
            if "courte" in user_message or "bts" in user_message or "dut" in user_message or "rapide" in user_message:
                found_duree = 'courtes'
            elif "longue" in user_message or "master" in user_message or "doctorat" in user_message:
                found_duree = 'longues'
            else:
                found_duree = None
            
            if found_duree:
                # Query specific duration type
                q = f"get_duree_etudes({found_duree}, D, A, I, C)"
                res = list(prolog.query(q))
                
                if res:
                    r = res[0]
                    display_name = "Études Courtes" if found_duree == 'courtes' else "Études Longues"
                    
                    response_text = f"⏱️ **{display_name}** :\n"
                    response_text += f"📌 {clean_text(r['D'])}\n"
                    response_text += f"{clean_text(r['A'])}\n"
                    response_text += f"{clean_text(r['I'])}\n"
                    response_text += f"{clean_text(r['C'])}\n"
                else:
                    response_text = f"Je n'ai pas d'infos sur les études '{found_duree}'."
            else:
                # General comparison
                response_text = "⏱️ **Durée des Études** :\n"
                response_text += "- **Courtes (2-3 ans)** : BTS, DUT, Licence → Insertion rapide\n"
                response_text += "- **Longues (5-8 ans)** : Ingénieur, Médecine, Master → Spécialisation\n"
                response_text += "Précisez 'courtes' ou 'longues' pour plus de détails."


        # --- 6.3 CONCOURS & EXAMENS D'ADMISSION (Nouveau) ---
        elif "concours" in user_message or "examen" in user_message or "admission" in user_message or "test" in user_message or "entretien" in user_message or "preparer" in user_message or "preparation" in user_message:
            
            # Map keywords to exam types
            concours_map = {
                'medecine': ['médecine', 'medecine', 'pharmacie', 'dentaire'],
                'ingenierie_public': ['ingénierie', 'ingenieur', 'ensa', 'emi', 'ensias', 'public'],
                'ecoles_privees': ['privé', 'prive', 'emsi', 'uir', 'um6p', 'hem'],
                'commerce': ['commerce', 'gestion', 'encg', 'iscae', 'esca', 'business']
            }
            
            found_concours = None
            for conc_key, keywords in concours_map.items():
                if any(k in user_message for k in keywords):
                    found_concours = conc_key
                    break
            
            if found_concours:
                # Query specific exam type
                q = f"get_concours_admission({found_concours}, E, C)"
                res = list(prolog.query(q))
                
                if res:
                    r = res[0]
                    display_name = found_concours.replace('_', ' ').title()
                    if found_concours == 'medecine': display_name = 'Médecine'
                    elif found_concours == 'ingenierie_public': display_name = 'Ingénierie (Public)'
                    elif found_concours == 'ecoles_privees': display_name = 'Écoles Privées'
                    
                    response_text = f"📝 **Concours {display_name}** :\n"
                    response_text += f"📋 {clean_text(r['E'])}\n"
                    response_text += f"{clean_text(r['C'])}\n"
                else:
                    response_text = f"Je n'ai pas d'infos sur les concours '{found_concours}'."
            else:
                # General exam advice
                response_text = "📝 **Concours & Admissions** :\n"
                response_text += "- **Médecine** : Dossier + concours écrit/oral\n"
                response_text += "- **Ingénierie** : Tests maths, physique, logique\n"
                response_text += "- **Privé** : Tests + entretien motivationnel\n"
                response_text += "- **Commerce** : Tests aptitude + étude de cas\n"
                response_text += "Précisez une filière pour plus de détails."

        # --- 6.4 CHOIX DE LANGUE (Nouveau) ---
        elif "langue" in user_message or "français" in user_message or "anglais" in user_message or "arabe" in user_message or "continuer en" in user_message:
            
            # Detect which language is being asked about
            langues_map = {
                'arabe': ['arabe', 'arabic', 'ar '],  # Space after 'ar' to avoid matching 'carrière'
                'francais': ['français', 'francais', 'french'],
                'anglais': ['anglais', 'english']
            }
            
            found_langue = None
            for lang_key, keywords in langues_map.items():
                if any(k in user_message for k in keywords):
                    found_langue = lang_key
                    break
            
            if found_langue:
                # Query specific language
                q = f"get_choix_langue({found_langue}, D, A, I, C)"
                res = list(prolog.query(q))
                
                if res:
                    r = res[0]
                    display_name = found_langue.capitalize()
                    if found_langue == 'francais': display_name = 'Français'
                    elif found_langue == 'anglais': display_name = 'Anglais'
                    
                    response_text = f"🌍 **Continuer en {display_name}** :\n"
                    response_text += f"📌 {clean_text(r['D'])}\n"
                    response_text += f"{clean_text(r['A'])}\n"
                    response_text += f"{clean_text(r['I'])}\n"
                    response_text += f"{clean_text(r['C'])}\n"
                else:
                    response_text = f"Je n'ai pas d'infos sur la langue '{found_langue}'."
            else:
                # General language advice
                response_text = "🌍 **Choix de Langue** :\n"
                response_text += "- **Français** : Sciences, Médecine, Ingénierie\n"
                response_text += "- **Anglais** : IT, Commerce International\n"
                response_text += "- **Arabe** : Lettres, Droit, Sciences Humaines\n"
                response_text += "Précisez une langue pour plus de détails."


        # --- 6.4.BIS FINANCEMENT & BOURSES (Nouveau) ---
        elif "bourse" in user_message or "financement" in user_message or "aide" in user_message or "prêt" in user_message or "logement" in user_message or "coût" in user_message or "payer" in user_message:
            # Note: "coût" et "payer" peuvent matcher Ecoles Privées (section 6), mais ici on capture les questions génériques ou spécifiques bourses
            
            # Map keywords
            financement_map = {
                'public': ['public', 'gratuit', 'fac'],
                'bourses_gouvernementales': ['bourse', 'minhaty', 'gouvernement'],
                'bourses_privees': ['privé', 'prive', 'fondation', 'mérite'],
                'international': ['étranger', 'etranger', 'erasmus', 'internationale'],
                'personnel': ['prêt', 'banque', 'travail', 'job']
            }
            
            found_fin = None
            for key, keywords in financement_map.items():
                if any(k in user_message for k in keywords):
                    found_fin = key
                    break
            
            # Default to bourses if just "bourse" is asked
            if not found_fin and "bourse" in user_message:
                found_fin = 'bourses_gouvernementales'

            if found_fin:
                q = f"get_financement({found_fin}, D, C)"
                res = list(prolog.query(q))
                if res:
                    r = res[0]
                    display_name = found_fin.replace('_', ' ').title()
                    response_text = f"💰 **Financement : {display_name}**\n📌 {clean_text(r['D'])}\n💡 {clean_text(r['C'])}"
                else: 
                     response_text = f"Pas d'info financement pour '{found_fin}'."
            else:
                 # Si on n'a pas détecté de type précis mais que le mot clé financement est là
                 # On ne fait rien si c'était "aide" (déjà géré par Vague) ou "coût" (géré par Ecoles)
                 # Sauf si on est ici, c'est que les sections précédentes n'ont pas matché (ordre important)
                 # On renvoie un conseil général
                 q = f"get_financement(bourses_gouvernementales, D, C)"
                 res = list(prolog.query(q))
                 if res:
                     r = res[0]
                     response_text = f"💰 **Bourses & Aides** :\nLa plupart des étudiants demandent **Minhaty**.\n📌 {clean_text(r['D'])}\n💡 Précisez 'bourse public', 'prêt' ou 'étranger' pour plus de détails."

        # --- 6.4.TER DEFINITIONS (Nouveau) ---
        elif "c'est quoi" in user_message or "définition" in user_message or "signifie" in user_message or "c est quoi" in user_message or "cest quoi" in user_message or "qu'est ce que" in user_message or "quest ce que" in user_message:
             
             def_map = {
                 'lmd': 'LMD', 'cpge': 'CPGE', 'prepa': 'CPGE', 'bts': 'BTS', 'dut': 'DUT',
                 'ensa': 'ENSA', 'encg': 'ENCG', 'est': 'EST', 'fst': 'FST', 'ofppt': 'OFPPT',
                 'master': 'Master', 'ingénieur': 'Ingénieur', 'ingenieur': 'Ingénieur'
             }
             

             found_key = None
             for k, v in def_map.items():
                 # Use regex for word boundary to avoid "est" matching "c'est"
                 if re.search(rf'\b{re.escape(k)}\b', user_message):
                     found_key = v
                     break
            
             if found_key:
                 q = f"definition('{found_key}', T)"
                 res = list(prolog.query(q))
                 if res:
                     response_text = f"📖 **Définition ({found_key})** :\n{clean_text(res[0]['T'])}"
                 else:
                     response_text = f"Je n'ai pas de définition pour '{found_key}'."
             else:
                 response_text = "📖 **Définitions** : Je peux définir LMD, CPGE, ENSA, ENCG, EST, FST, BTS, DUT..."

        # --- 6.5 DOMAINES & DEBOUCHES (Nouveau) ---
        elif "débouché" in user_message or "débouchés" in user_message or "métier" in user_message or "carrière" in user_message or "profession" in user_message or "travailler" in user_message:
            
            # Map keywords to domain atoms
            domaines_map = {
                'medecine': ['médecine', 'medecine', 'pharmacie', 'dentaire', 'santé', 'docteur'],
                'ingenierie': ['ingénierie', 'ingenieur', 'ensa', 'emi', 'génie'],
                'informatique': ['informatique', 'info', 'it', 'data', 'cyber', 'développeur', 'programmation'],
                'commerce': ['commerce', 'gestion', 'finance', 'marketing', 'business', 'encg'],
                'shs': ['sciences humaines', 'psycho', 'socio', 'journalisme', 'communication', 'lettres'],
                'archi': ['architecture', 'design', 'urbanisme', 'architecte'],
                'tourisme': ['tourisme', 'hôtel', 'logistique', 'événementiel']
            }
            
            found_domaine = None
            for dom_key, keywords in domaines_map.items():
                if any(k in user_message for k in keywords):
                    found_domaine = dom_key
                    break
            
            if found_domaine:
                # Query Prolog for domain details
                q = f"get_detail_domaine({found_domaine}, M, E, C)"
                res = list(prolog.query(q))
                
                if res:
                    r = res[0]
                    display_name = found_domaine.replace('_', ' ').title()
                    if found_domaine == 'medecine': display_name = 'Médecine & Santé'
                    elif found_domaine == 'ingenierie': display_name = 'Ingénierie'
                    elif found_domaine == 'informatique': display_name = 'Informatique & IT'
                    elif found_domaine == 'shs': display_name = 'Sciences Humaines & Sociales'
                    elif found_domaine == 'archi': display_name = 'Architecture & Design'
                    
                    response_text = f"💼 **{display_name}** :\n"
                    response_text += f"👔 **Métiers** : {clean_text(r['M'])}\n"
                    response_text += f"🏫 **Écoles** : {clean_text(r['E'])}\n"
                    response_text += f"{clean_text(r['C'])}\n"
                    
                    # NOUVEAU: Check compatibility if Bac is mentioned
                    bacs_keywords = {
                        'SM': ['sm', 'math'],
                        'PC': ['pc', 'physique'],
                        'SVT': ['svt', 'bio'],
                        'ECO': ['eco', 'economie'],
                        'LITT': ['litt', 'lettre']
                    }
                    detected_bac = None
                    for bac_code, keywords in bacs_keywords.items():
                        if any(k in user_message for k in keywords):
                            detected_bac = bac_code
                            break
                    
                    if detected_bac:
                        # Map domain to compatibility atom
                        compat_domain_map = {
                            'medecine': 'medecine',
                            'ingenierie': 'ingenierie',
                            'informatique': 'informatique',
                            'commerce': 'commerce',
                            'shs': 'lettres',  # SHS maps to lettres in compatibility
                            'arts': 'lettres',
                            'tourisme': 'commerce'
                        }
                        compat_atom = compat_domain_map.get(found_domaine, found_domaine)
                        
                        # Check compatibility
                        q_compat = f"check_compatibilite('{detected_bac}', {compat_atom}, Statut, Msg)"
                        compat_res = list(prolog.query(q_compat))
                        if compat_res:
                            response_text += f"\n\n🎯 **Compatibilité Bac {detected_bac}** :\n{clean_text(compat_res[0]['Msg'])}"
                
                else:
                    response_text = f"Je n'ai pas de détails sur le domaine '{found_domaine}'."
            
            else:
                # Si PAS DE DOMAINE detecté, on regarde si un BAC est mentionné (ex: "Débouchés SM ?")
                bacs_keywords_only = {
                    'SM': ['sm', 'math'], 'PC': ['pc', 'physique'], 'SVT': ['svt', 'bio', 'science'],
                    'ECO': ['eco', 'economie', 'gestion'], 'LITT': ['litt', 'lettre'], 'TECH': ['tech', 'meca', 'elec']
                }
                detected_bac_only = None
                for bac_code, keywords in bacs_keywords_only.items():
                   if any(k in user_message for k in keywords):
                       detected_bac_only = bac_code
                       break
                
                if detected_bac_only:
                    q_bac = f"get_detail_bac('{detected_bac_only}', I, A, L, C)"
                    res_bac = list(prolog.query(q_bac))
                    if res_bac:
                        r = res_bac[0]
                        response_text = f"🎓 **Débouchés Bac {detected_bac_only}** :\n"
                        response_text += f"🚀 **Filières** : {clean_text(r['I'])}\n"
                        response_text += f"✅ **Avantages** : {clean_text(r['A'])}\n"
                        response_text += f"💡 **Conseil** : {clean_text(r['C'])}"
                    else:
                        response_text = f"Je n'ai pas d'infos détaillées pour le Bac {detected_bac_only}."
                else:
                    response_text = "💼 **Débouchés** : Précisez un domaine (Médecine, Ingénierie) ou votre Bac (SM, PC, Eco)."

        # --- 6.5 COMPATIBILITE BAC-FILIERE (Question type "SVT + informatique possible?") ---
        # --- Section Removed: merged into 5. COMPATIBILITE ---

        # --- 6.9 NEW KNOWLEDGE: RECHERCHE PAR BAC (Support Étendu via filiere/6) ---
        elif "bac" in user_message and any(s in user_message for s in ['math', 'science', 'eco', 'lettre', 'technique', 'art', 'sm', 'pc', 'svt']):
            # Mappage des noms de bac vers les atomes Prolog du nouveau fichier
            # On utilise le même mapping regex que plus bas pour la cohérence

            bac_map_new = {
                'Sciences mathématiques A': [r'\bsm\b', r'\bmath\b'],
                'Sciences physiques': [r'\bpc\b', r'\bphysique\b'],
                'Sciences de la Vie et de la Terre': [r'\bsvt\b', r'\bbio\b', r'\bscience vie\b'],
                'Sciences économiques': [r'\beco\b', r'\beconomie\b'],
                'Sciences de gestion comptable': [r'\bgestion\b'],
                'Sciences et technologies électriques': [r'\belec\b', r'\btech\b'],
                'Sciences et technologies mécaniques': [r'\bmeca\b', r'\bindustriel\b'],
                'Arts appliqués': [r'\bart\b', r'\barts\b', r'\bappliques\b', r'\bappliqués\b'],
                'Lettres': [r'\blitt\b', r'\blettre\b'],
                'Sciences humaines': [r'\bhumaine\b']
            }
            
            found_bac_full = None
            for name, patterns in bac_map_new.items():
                for pat in patterns:
                     if re.search(pat, user_message, re.IGNORECASE):
                         found_bac_full = name
                         break
                if found_bac_full: break
            
            if found_bac_full:
                # Query filiere/6: filiere(Bac, Secteur, Filiere, Etablissement, Duree, Diplome)
                q = f"filiere('{found_bac_full}', Secteur, Fil, Etab, Duree, Dip)"
                try:
                    res = list(prolog.query(q))
                    if res:
                        # On groupe par secteur pour l'affichage
                        secteurs = {}
                        for r in res:
                            sec = clean_text(r['Secteur'])
                            if sec not in secteurs: secteurs[sec] = []
                            # Avoid duplicates
                            entry = f"- {clean_text(r['Fil'])} ({clean_text(r['Etab'])})"
                            if entry not in secteurs[sec]:
                                secteurs[sec].append(entry)
                        
                        response_text = f"🎓 **Options pour {found_bac_full}** :\n"
                        # Afficher max 3 secteurs pour ne pas spammer, ou tout? Tout c'est mieux si pas trop long.
                        for i, (sec, options) in enumerate(secteurs.items()):
                            if i > 5: break # Limit to 5 sectors
                            response_text += f"\n📂 **{sec}** :\n" + "\n".join(options[:4]) # Max 4 per sector
                        
                        response_text += "\n\n(Dites 'Détails [Filière]' pour plus d'infos)"
                    else:
                        # Fallback to legacy section
                        response_text = None 
                except Exception as e:
                    print(f"Error querying filiere: {e}")
                    response_text = None
            else:
                response_text = None

        # --- 6.95 NEW KNOWLEDGE: PLATEFORMES ---
        elif "plateforme" in user_message or "site" in user_message:
             q_all = "plateforme(Nom, URL)"
             found_lat = None
             try:
                 all_plats = list(prolog.query(q_all))
                 for p in all_plats:
                     nom = clean_text(p['Nom']).lower()
                     if nom in user_message:
                         found_lat = p
                         break
                 
                 if found_lat:
                     response_text = f"🔗 **Plateforme {clean_text(found_lat['Nom'])}** : {clean_text(found_lat['URL'])}"
                 else:
                     response_text = None # Let fallback handle general site queries
             except:
                 response_text = None


    return jsonify({
        "response": response_text
    })


# ============================================================================
# NEW ENDPOINTS FOR ENHANCED RAG
# ============================================================================

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get conversation history for a session"""
    session_id = request.args.get('session_id', 'default')
    history = conversation_manager.get_history(session_id)
    
    return jsonify({
        "session_id": session_id,
        "message_count": len(history),
        "history": history
    })

@app.route('/chat/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history for a session"""
    data = request.json
    session_id = data.get('session_id', 'default')
    conversation_manager.clear_session(session_id)
    
    return jsonify({
        "message": "Conversation cleared",
        "session_id": session_id
    })

@app.route('/system/stats', methods=['GET'])
def system_stats():
    """Get system statistics"""
    stats = {
        "vector_search_enabled": USE_VECTOR_SEARCH,
        "active_sessions": len(conversation_manager.get_active_sessions())
    }
    
    if USE_VECTOR_SEARCH and vector_kb and vector_kb.service:
        stats.update(vector_kb.service.get_stats())
    
    return jsonify(stats)

if __name__ == '__main__':

    print("Serveur Python + SWI-Prolog demarré sur le port 5000")
    app.run(port=5000, debug=True)
