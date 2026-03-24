"""
YAFI Chatbot - OPTIMIZED SERVER V2
<<<<<<< HEAD
Focus: Ollama FIRST, then Prolog/Hard-coded as FALLBACK
================================
PRIORITY ORDER:
1. Trivial questions (YAFI definition, thanks, etc) -> Return immediately
2. OLLAMA ADVANCED (Smart, context-aware, intelligent) -> TRY FIRST
3. Prolog + Hard-coded -> Fallback if Ollama has insufficient data

This solves: "Hard-coded responses were blocking Ollama!"
=======
--------------------------------
PRIORITY ORDER:
1. Trivial questions -> Return immediately
2. Specialized Intents (Prolog Benchmarking, Fees, etc) -> HIGH PRIORITY
3. Ollama Advanced (RAG) -> FALLBACK if no specific intent
4. Generic Fallback
>>>>>>> 3257fc1 (final)
"""

import sys
import os
from dotenv import load_dotenv
<<<<<<< HEAD

# Load .env from project root
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
load_dotenv(os.path.join(root_dir, ".env"))

sys.path.insert(0, base_dir)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog
import re
import random
from conversation_manager import conversation_manager
from vector_knowledge import VectorKnowledgeBase
from response_builder import ResponseBuilder
=======
import json
import re
import random
import time
import threading
import unicodedata
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pyswip import Prolog

# Custom Modules
from conversation_manager import conversation_manager
from vector_knowledge import VectorKnowledgeBase
>>>>>>> 3257fc1 (final)
from llm_engine import llm_engine
from enhanced_rag import rag_system
from intent_classifier import IntentClassifier
from entity_extractor import entity_extractor
import user_memory

<<<<<<< HEAD
=======
# Load environment
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
load_dotenv(os.path.join(root_dir, ".env"))
sys.path.insert(0, base_dir)

>>>>>>> 3257fc1 (final)
app = Flask(__name__)
CORS(app)

# ============================================================================
# INITIALIZATION
# ============================================================================

prolog = Prolog()
<<<<<<< HEAD
base_dir = os.path.dirname(os.path.abspath(__file__))
# Knowledge Base: Use the full consolidated system only to avoid Redefined procedure warnings
prolog.consult(os.path.join(base_dir, "full_orientation_system.pl").replace('\\', '/'))

# Components Initialization
# Note: These use singleton instances from their respective modules
vector_kb = rag_system.vector_kb
intent_classifier = IntentClassifier()

# Ollama Global Status Helper
def is_ollama_available():
    return llm_engine.enabled and llm_engine.health_check()['available']

print(f"✅ AI Components Initialized")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_text(text):
    """Clean text output from Prolog"""
=======
prolog_lock = threading.Lock()
# Knowledge Base
prolog.consult(os.path.join(base_dir, "full_orientation_system.pl").replace('\\', '/'))

# Components
vector_kb = rag_system.vector_kb
intent_classifier = IntentClassifier()

def is_ollama_available():
    return llm_engine.enabled and llm_engine.health_check()['available']

def safe_query(query_str):
    """Thread-safe wrapper for Prolog queries"""
    with prolog_lock:
        return list(prolog.query(query_str))

def clean_text(text):
>>>>>>> 3257fc1 (final)
    if isinstance(text, str):
        return text.replace("\\n", "\n").strip()
    return str(text)

def normalize_text(text):
<<<<<<< HEAD
    """Normalize text for matching (remove accents)"""
    import unicodedata
    if not isinstance(text, str):
        return str(text)
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def found_context_match(key_dict, user_msg, last_topic):
    """Find match in dictionary using user_msg or last topic"""
    for k, v in key_dict.items():
        if k in user_msg.lower(): return v
    if last_topic:
        for k, v in key_dict.items():
            if k in last_topic.lower(): return v
    return None

# ============================================================================
# MAIN CHAT ENDPOINT - OPTIMIZED
=======
    if not isinstance(text, str): return str(text)
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

# --- AXE 5 HELPERS ---
KNOWN_ENTITIES = [
    "emsi", "uir", "um6p", "ensa", "encg", "fst", "ensias", "iscae", "uic", "fmp", "fmd",
    "ensam", "ensck", "isss", "ispits", "enam", "iav", "ispm", "itsat", "isic", "inau",
    "isadac", "esba", "inba", "insap", "aat", "isitt", "imsk", "iss", "issf", "irfcjs",
    "ena", "est", "ests", "ofppt", "medecine", "pharmacie", "architecture", "minhaty", "bts", "dut",
    "ehtp", "inpt", "emi", "lydex", "supinfo", "hem", "esca", "uiass", "upsat", "eac", "arm", "eri",
    "casablanca", "rabat", "marrakech", "tanger", "agadir", "fes", "meknes", "oujda", "kenitra",
    "tetouan", "safi", "el jadida", "beni mellal", "settat", "khouribga", "nador", "taza",
    "errachidia", "benguerir", "ifrane", "mohammedia", "uik", "cursussup",
    "commerce", "management", "ingenierie", "droit", "science", "technique"
]

def sanitize_prolog(text):
    """Sanitize strings for Prolog to prevent injections and syntax errors"""
    if not text: return ""
    return str(text).replace("'", "''")

def normalize_school_id(name):
    """Normalize user input to internal school IDs with alias handling"""
    if not name: return ""
    name_low = name.lower().strip()
    
    # Direct alias map
    aliases = {
        'polytechnique agadir': 'uik',
        'isiam': 'uik',
        'universiapolis': 'uik',
        'ecole de medecine': 'medecine',
        'faculte de medecine': 'medecine'
    }
    
    for alias, sid in aliases.items():
        if alias in name_low: return sid
        
    # Standard cleanup
    name_clean = name_low.replace('ecole', '').replace('faculté', '').replace('faculte', '').strip()
    
    # Generic Acronyms Check
    generic_sigles = ["encg", "ensa", "fst", "est", "ensam", "bts"]
    if name_clean in generic_sigles:
        return name_clean

    # Priority matching keywords
    if 'iscae' in name_clean: return 'iscae'
    if 'ensam' in name_clean: return 'ensam'
    if 'enam' in name_clean: return 'enam'
    if 'ensias' in name_clean: return 'ensias'
    if 'ehtp' in name_clean: return 'ehtp'
    if 'inpt' in name_clean: return 'inpt'
    if 'emsi' in name_clean: return 'emsi' # Handle EMSI before EMI to avoid substring collision
    if 'emi' in name_clean: return 'emi'
    if 'ensa' in name_clean: return 'ensa'
    if 'ests' in name_clean or ('est' in name_clean and 'safi' in name_clean): return 'ests'

    # Check all known specific schools globally
    for s in sorted(KNOWN_ENTITIES, key=len, reverse=True):
        if s in name_clean:
            return s
            
    # Return cleaned sigle if brief
    if len(name_clean.split()) <= 2:
        return name_clean.replace(" ", "_")
    
    return ""

# ============================================================================
# CHAT ENDPOINT
>>>>>>> 3257fc1 (final)
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
<<<<<<< HEAD
    """
    Optimized chat handler:
    1. Trivial → Immediate return
    2. Ollama Advanced → TRY FIRST (if enabled)
    3. Prolog + Hard-coded → Fallback
    """
    import time
    start_time = time.time()
    
    data = request.json
    user_message = data.get('message', '').lower().strip()
    current_session_id = data.get('session_id', 'default')
    
    print(f"\n📨 NEW MESSAGE: '{user_message[:50]}...'")
    
    # ========================================================================
    # PHASE 0: MEMORY & ENTITY EXTRACTION
    # ========================================================================
    
    # 1. Load persistent profile from Supabase/Local JSON
    profile = user_memory.load(current_session_id)
    
    # 2. Extract entities from current message
    entities = entity_extractor.extract(user_message)
    if entities:
        print(f"  💎 Extracted Entities: {entities}")
        # 3. Update persistent profile
        profile = user_memory.update(current_session_id, entities)
    
    response_text = None
    
    # ========================================================================
    # PHASE 1: TRIVIAL RESPONSES (Return immediately)
    # ========================================================================
    
    print("PHASE 1: Checking trivial questions...")
    
    # YAFI définition
    if any(kw in user_message for kw in ['yafi', 'y.a.f.i', 'y a f i']):
        response_text = "✨ **YAFI** est l'acronyme des créateurs avec **I** pour **Intelligence**!\n\nUn chatbot d'orientation post-bac pour les étudiants marocains. 🎓"
    
    # Politeness
    elif user_message in ['merci', 'thank you', 'merci beaucoup']:
        response_text = "De rien ! 😊 Des questions d'orientation ?"
    
    elif user_message in ['oui', 'non', 'ok']:
        response_text = "Compris ! Autres questions ?"
    
    if response_text:
        elapsed = round((time.time() - start_time) * 1000)
        print(f"✓ Trivial match → Returning immediately ({elapsed}ms)")
        user_memory.add_message(current_session_id, 'user', user_message)
        user_memory.add_message(current_session_id, 'assistant', response_text)
        return jsonify({"response": response_text, "response_time_ms": elapsed})
    
    # ========================================================================
    # PHASE 2: OLLAMA ADVANCED (Try if enabled)
    # ========================================================================
    
    print("PHASE 2: Trying Ollama Advanced...")
    
    if is_ollama_available():
        try:
            print("  Calling Enhanced RAG (Ollama) with Profile Context...")
            # Pass the profile for contextual awareness
            rag_result = rag_system.generate_response(
                user_message,
                session_id=current_session_id,
                profile=profile
            )
            
            ollama_response = rag_result.get("response", "")
            
            if ollama_response:
                # AGENTIC TOOL CALL: Detect Prolog Evaluate
                if "[PROLOG_EVALUATE:" in ollama_response:
                    print("  🛠️ TOOL CALL DETECTED: Prolog Evaluate")
                    try:
                        match = re.search(r"\[PROLOG_EVALUATE:\s*(.*?)\]", ollama_response)
                        if match:
                            # --- PHASE 3: Slot Filling from Memory ---
                            params_str = match.group(1)
                            regex_params = dict(re.findall(r"(\w+)=([\w.]+)", params_str))
                            
                            # Priority: Tag Params > Extracted Entities > Profile Memory > Defaults
                            # We merge them: Profile is base, then Extracted, then Tag overrides
                            final_params = {
                                'bac': profile.get('bac'),
                                'moyenne': profile.get('moyenne'),
                                'ville': profile.get('ville'),
                                'budget': profile.get('budget'),
                                'ecole': profile.get('ecole')
                            }
                            # Override with what we have
                            final_params.update({k: v for k, v in (entities or {}).items() if v is not None})
                            final_params.update({k: v for k, v in regex_params.items() if v not in [None, 'CODE', 'VALEUR', 'NOM', 'SIGLE']})
                            
                            bac = str(final_params.get('bac') or 'PC').upper()
                            moyenne = final_params.get('moyenne') or '14'
                            budget = final_params.get('budget') or '50000'
                            ville = str(final_params.get('ville') or 'Casablanca').capitalize()
                            ecole = str(final_params.get('ecole') or 'ENSA').upper()
                            
                            # Execute Prolog Query
                            q = f"calculer_score_orientation('{bac}', {moyenne}, {budget}, '{ville}', '{ecole}', Score)"
                            prolog_res = list(prolog.query(q))
                            
                            if prolog_res:
                                score = prolog_res[0].get('Score', 0)
                                expert_verdict = f"\n\n--- \n🔍 **Verdict de l'Expert Prolog** :\n"
                                expert_verdict += f"D'après mes calculs formels, ton score d'affinité pour **{ecole}** est de **{score}%**.\n"
                                expert_verdict += f"(Données utilisées: Bac {bac}, moyenne {moyenne}, budget {budget} DH, ville {ville})"
                                
                                response_text = ollama_response.replace(match.group(0), expert_verdict)
                                
                                # Update profile with the school used
                                if ecole:
                                    user_memory.update(current_session_id, {"ecole": ecole})
                            else:
                                response_text = ollama_response.replace(match.group(0), "\n\n(Calcul expert impossible : paramètres manquants)")
                        else:
                            response_text = ollama_response
                    except Exception as e_tool:
                        print(f"  ❌ Tool Execution Error: {e_tool}")
                        response_text = ollama_response 
                else:
                    response_text = ollama_response
                
                print(f"✓ Ollama responded ({len(response_text)} chars)")
            else:
                response_text = None
                
        except Exception as e:
            print(f"  ❌ Ollama error: {e}")
            response_text = None
    
    # ========================================================================
    # PHASE 3: PROLOG + HARD-CODED (Fallback)
    # Only if Ollama failed or is disabled
    # ========================================================================
    
    if not response_text:
        print("PHASE 3: Falling back to Prolog/Hard-coded...")
        try:
            # 1. Check for hard-coded abbreviations first
            if user_message in ['cv', 'c v', 'curriculum']:
                response_text = "📝 **CV Étudiant** :\n- Infos personnelles\n- Formation\n- Compétences\n- Expériences\n\n💡 Gardez 1 page max !"
            elif user_message in ['ensa', 'e n s a']:
                response_text = "🏫 **ENSA** - École Nationale des Sciences Appliquées\n\nÉcoles d'ingénierie publiques au Maroc.\n📍 Villes multiples\n✅ Admission : Bac+Concours\n💰 GRATUIT (Public)"
            elif user_message in ['emsi', 'e m s i']:
                response_text = "🏫 **EMSI** - École Marocaine des Sciences de l'Ingénieur\n\n💼 Privée, IT & Ingénierie\n💰 ~35-45k DH/an"
            elif any(kw in user_message for kw in ['qui t\'a cree', 'qui a cree', 'createur', 'adam moufrije']):
                response_text = "👨‍💻 **Adam Moufrije** - Créateur & Développeur\n\nUtilisant Ollama pour l'IA ! 🤖"
            elif any(kw in user_message for kw in ['bonjour', 'bjr', 'hello', 'hi']):
                greetings = [
                    "Bonjour ! 👋 Comment puis-je vous aider ?",
                    "Bonjour ! 🎓 Prêt pour parler orientation ?",
                    "Hey ! Quoi de neuf ?"
                ]
                response_text = random.choice(greetings)
            elif any(kw in user_message for kw in ['bac pc', 'bac sm', 'bac svt', 'bac eco', 'orientation']):
                # Try Prolog for BAC-specific questions
                bac_match = None
                for code in ['SM', 'PC', 'SVT', 'ECO', 'LITT']:
                    if code.lower() in user_message:
                        bac_match = code
                        break
                
                if bac_match:
                    q = f"get_detail_bac('{bac_match}', I, A, L, C)"
                    res = list(prolog.query(q))
                    if res:
                        d = res[0]
                        response_text = f"🎓 **BAC {bac_match}** :\n"
                        response_text += f"{clean_text(d['I'])}\n{clean_text(d['A'])}\n{clean_text(d['C'])}"
            else:
                # 2. Try Prolog for general queries
                # Escape single quotes for Prolog
                safe_message = user_message.lower().replace("'", "''")
                # We use a simplified regex approach for common Prolog patterns if needed
                # But here we just try a general expert_respond rule if it exists
                q = f"expert_respond('{safe_message}', Resultat)"
                try:
                    res = list(prolog.query(q))
                    if res:
                        response_text = res[0]['Resultat']
                except:
                    pass
            
            if not response_text:
                # Last resort: generic helpful response
                response_text = "Je n'ai pas trouvé de réponse précise, mais je peux t'aider pour l'orientation ENSA, FST, Médecine ou d'autres écoles au Maroc. Peux-tu préciser ta question ?"
                
        except Exception as e_fallback:
            print(f"  ❌ Fallback Error: {e_fallback}")
            response_text = "Désolé, je rencontre une difficulté technique. Peux-tu reformuler ta question sur l'orientation ?"

    # ========================================================================
    # SAVE HISTORY & RETURN
    # ========================================================================
    
    user_memory.add_message(current_session_id, 'user', user_message)
    user_memory.add_message(current_session_id, 'assistant', response_text)
    
    # Calculate score/ecole for the API response
    final_score = score if ('score' in locals() and score is not None and score > 0) else None
    final_ecole = ecole if ('final_score' in locals() and final_score is not None) else None

    elapsed = round((time.time() - start_time) * 1000)
    print(f"⏱️ Response time: {elapsed}ms")

    return jsonify({
        "response": response_text, 
        "response_time_ms": elapsed,
        "source": "ollama_advanced" if ("ollama_response" in locals() and response_text == ollama_response) else "prolog_expert",
        "score": final_score,
        "ecole": final_ecole,
        "entities": entities
    })

# ============================================================================
# TEST ENDPOINTS
# ============================================================================

@app.route('/test/ollama', methods=['GET'])
def test_ollama():
    """Test if Ollama is working"""
    if not is_ollama_available():
        return jsonify({"status": "disabled", "message": "Ollama not initialized"}), 503
    
    try:
        test_response = rag_system.generate_response("Bonjour, comment ça va ?", use_llm=True)
        response_text = test_response.get("response", "")
        return jsonify({
            "status": "working",
            "response_preview": response_text[:100] + "..."
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/test/prolog', methods=['GET'])
def test_prolog():
    """Test if Prolog is working"""
    try:
        res = list(prolog.query("yafi_definition(X)"))
        if res:
            return jsonify({"status": "working", "prolog_result": str(res[0])})
        else:
            return jsonify({"status": "no_data", "message": "Prolog queries work but no YAFI data"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/test/components', methods=['GET'])
def test_components():
    """Test all components"""
=======
    start_time = time.time()
    data = request.json or {}
    user_message = data.get('message', '').lower().strip()
    current_session_id = data.get('session_id', 'default')
    should_stream = data.get('stream', False)
    
    # --- PHASE 0: RECEPTION & NORMALISATION ---
    print(f"[PHASE 0] Reception & Normalisation: '{user_message[:30]}...'")
    user_message_normalized = normalize_text(user_message)
    msg_low = user_message_normalized.lower()
    
    # --- PHASE -1: EARLY SAFETY GUARD ---
    print(f"[PHASE -1] Safety Guard (Blocklist check)")
    OFF_TOPIC_KEYWORDS = [
        "recette", "tajine", "couscous", "cuisine", "cuisson", "ingrédient",
        "football", "match", "météo", "température", "pluie", "quel temps", "il fait chaud",
        "politique", "élection", "vote", "président",
        "film", "série", "netflix", "musique", "chanson",
        "jeu vidéo", "playstation", "xbox", "fortnite",
        "visa", "études étrangères", "bitcoin", "bourse crypto",
        "blague", "raconte moi une histoire", "poème", "qui est le plus fort"
    ]
    if any(kw in msg_low for kw in OFF_TOPIC_KEYWORDS):
        print(f"  !! BLOCK Phase -1 active !!")
        resp_data = {
            "response": "🎓 Je suis YAFI, assistant d'orientation au **MAROC uniquement**. Cette question ne relève pas de mon domaine d'expertise académique.",
            "source": "phase_-1_safety_guard",
            "done": True
        }
        if should_stream:
            return Response(json.dumps(resp_data) + "\n", mimetype='application/x-ndjson')
        return jsonify(resp_data)
    
    # --- PHASE 1: ENTITY EXTRACTION & MEMORY ---
    print(f"[PHASE 1] Entity Extraction & Memory Sync")
    profile = user_memory.load(current_session_id)
    entities = entity_extractor.extract(user_message)
    if entities:
        profile = user_memory.update(current_session_id, entities)
    
    current_entity = (entities.get('ecole') or '').lower().strip() if isinstance(entities, dict) else None
    
    # Mémoire contextuelle
    if not current_entity and profile and profile.get('ecole'):
        current_entity = str(profile.get('ecole')).lower().strip()
        print(f"DEBUG: Pulled current_entity '{current_entity}' from Memory!")
    
    # Brute-force entity detection as safety net (High Priority Overrides)
    found_brute = None
    if 'ests' in msg_low or 'est safi' in msg_low: found_brute = 'ests'
    elif 'um6p' in msg_low: found_brute = 'um6p'
    elif 'emsi' in msg_low: found_brute = 'emsi'
    elif 'uir' in msg_low or 'universite internationale de rabat' in msg_low: found_brute = 'uir'
    elif 'ensa' in msg_low: found_brute = 'ensa'
    elif 'encg' in msg_low: found_brute = 'encg'
    elif 'iscae' in msg_low: found_brute = 'iscae'
    elif 'enam' in msg_low: found_brute = 'enam'
    elif 'uik' in msg_low or 'universiapolis' in msg_low: found_brute = 'uik'
    elif 'isitt' in msg_low: found_brute = 'isitt'
    elif 'ehtp' in msg_low: found_brute = 'ehtp'
    elif 'inpt' in msg_low: found_brute = 'inpt'
    elif 'insea' in msg_low: found_brute = 'insea'
    elif 'emi' in msg_low and 'emsi' not in msg_low: found_brute = 'emi'
    elif 'ena' in msg_low and 'ensa' not in msg_low: found_brute = 'ena'
    elif 'medecine' in msg_low or 'médecine' in msg_low: found_brute = 'medecine'
    elif 'architecture' in msg_low: found_brute = 'architecture'
    elif 'cursussup' in msg_low: found_brute = 'cursussup'
    elif 'minhaty' in msg_low: found_brute = 'minhaty'

    if found_brute:
        current_entity = found_brute
        print(f"DEBUG: Brute-force override active: '{current_entity}'")
    
    if not current_entity:
        current_entity = None
    else:
        # NEW LOGIC: ALWAYS SYNC BRUTE-FORCE ENTITY TO MEMORY TO PREVENT AMNESIA
        if str(profile.get('ecole')).lower().strip() != current_entity:
            profile = user_memory.update(current_session_id, {"ecole": current_entity})
            print(f"DEBUG: Saved '{current_entity}' to memory from brute-force/fallback!")

    detected_intent = None
    response_text = None
    expert_context = "" # New: Store facts for the LLM

    # --- PHASE 2: INTENT CLASSIFICATION ---
    print(f"[PHASE 2] Intent Classification")
    detected_intent = None
    print(f"DEBUG: Processing msg_low='{msg_low}'")
    
    # 1. High Priority Brute Force (Simulateur Admission)
    match_score_keywords = any(w in msg_low for w in ["score", "note", "seuil", "moyenne"])
    print(f"DEBUG: match_score_keywords={match_score_keywords}")
    if match_score_keywords:
        note_match = re.search(r"(1\d|20|10)", msg_low)
        print(f"DEBUG: note_match={note_match}")
        if note_match:
            detected_intent = "CALCULATE_SCORE"
            print(f"BRUTE FORCE MATCH: {detected_intent}")

    # 1b. Brute Force Safety Net
    if not detected_intent and any(w in msg_low for w in ["bourse", "financement", "argent", "payer"]):
        detected_intent = "SCHOLARSHIPS"
    if not detected_intent and any(w in msg_low for w in ["internat", "clubs", "cantine", "manger", "dormir", "vie"]):
        detected_intent = "CAMPUS_LIFE"
    if not detected_intent and any(w in msg_low for w in ["frais", "prix", "scolarite", "budget", "combien"]):
        detected_intent = "FINANCIALS"
    
    if not detected_intent and any(w in msg_low for w in ["bac pc", "bac svt", "bac sm", "bac eco", "bac lettres", "bac technique"]):
        detected_intent = "BAC_INFO"
    if not detected_intent and any(w in msg_low for w in ["conseil", "stratégie", "strategie", "que faire"]):
        detected_intent = "ORIENTATION_STRATEGY"

    if not detected_intent and intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)
        
    # 2. Comparison Brute Force Fallback
    if not detected_intent:
        if any(w in msg_low for w in ["comparer", "difference", " vs ", " entre "]):
            schools_found = [ent for ent in KNOWN_ENTITIES if ent in msg_low]
            if len(schools_found) >= 2:
                detected_intent = "COMPARE_SCHOOLS"
                print(f"BRUTE FORCE MATCH: {detected_intent}")

    # 3. Single School Intent Fallback
    if not detected_intent and any(w in msg_low for w in ["ville", "où se trouve", "situe", "emplacement", "opportunité", "concurrence"]):
        detected_intent = "CITY_INFOS"

    if not detected_intent and intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)

    print(f"  Intent: {detected_intent}, Entity: {current_entity}")

    source_detected = "hybrid_expert_llm" if detected_intent else "ollama_advanced"
    # ========================================================================
    # PHASE 2: SPECIALIZED EXPERT ROUTING (DETERMINISTIC FIRST)
    # ========================================================================
    expert_context = ""
    expert_found = False

    # 1. GEOGRAPHY & CITY SEARCH (High Priority)
    if not expert_found and (detected_intent in ["CITY_INFOS", "WHERE_TO_STUDY"] or any(c in msg_low for c in ["safi", "rabat", "casablanca", "casabla", "agadir", "marrakech", "fes", "tanger", "settat", "meknes", "benguerir"])):
        city_match = None
        for c in ["casablanca", "casabla", "rabat", "marrakech", "fes", "tanger", "agadir", "safi", "kenitra", "oujda", "settat", "meknes", "benguerir"]:
            if c in msg_low: 
                city_match = c if c != "casabla" else "casablanca"
                break
        
        if city_match:
            try:
                city_prolog = city_match.capitalize()
                # Exception withdrawn: Prolog uses 'Benguerir' without accent.
                
                res_loc = safe_query(f"localisation(S, '{city_prolog}')")
                if res_loc:
                    schools = sorted(list(set([r['S'].upper() for r in res_loc])))
                    
                    # Filter by Public/Private if requested
                    is_req_pub = any(w in msg_low for w in ["public", "publique"])
                    is_req_priv = any(w in msg_low for w in ["privé", "privee", "prive"])
                    
                    if is_req_pub or is_req_priv:
                        filtered = []
                        for s in schools:
                            dt = safe_query(f"detail_ecole('{s.lower()}', _, _, TF)")
                            if dt:
                                is_sch_pub = "public" in str(dt[0]['TF']).lower() or "gratuit" in str(dt[0]['TF']).lower()
                            else:
                                # Default to public if no detail is found unless explicitly known as private
                                is_sch_pub = s.lower() not in ["emsi", "uir", "uik", "supinfo", "hem", "esca", "uiass", "upsat", "eac", "isitt prive"]

                            if is_req_pub and is_sch_pub: filtered.append(s)
                            elif is_req_priv and not is_sch_pub: filtered.append(s)
                        if filtered: schools = filtered; stype_l = "Publiques" if is_req_pub else "Privées"; response_text = f"📍 **Établissements {stype_l} à {city_prolog} :**\n"
                        else: response_text = f"📍 **Établissements à {city_prolog} :**\n"
                    else:
                        response_text = f"📍 **Établissements à {city_prolog} :**\n"
                    
                    for s in schools: response_text += f"- {s}\n"
                    
                    res_opp = safe_query(f"ville_opportunite('{city_match}', O)")
                    if res_opp: response_text += f"\n💡 **Opportunités :** {clean_text(res_opp[0]['O'])}\n"
                    
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 1b. GLOBAL LIST (Reset Memory)
    if not expert_found and any(w in msg_low for w in ["list", "toutes les", "tous les", "chaque"]) and any(w in msg_low for w in ["école", "ecole", "universite", "etablissement"]):
        try:
            res = safe_query("etablissement(ID, _, _, _, _)")
            if res:
                all_ids = sorted(list(set([r['ID'].upper() for r in res])))[:15]
                response_text = "🏫 **Liste des établissements répertoriés :**\n"
                response_text += ", ".join(all_ids) + "...\n\n*Précise une école pour plus de détails.*"
                source_detected = "prolog_expert"
                expert_found = True
                current_entity = None # Reset sticky memory
                
                # Also reset physical JSON memory
                try:
                    p = user_memory.load(current_session_id)
                    p['ecole'] = None
                    p['entities'] = []
                    user_memory.save(current_session_id, p)
                except: pass

        except: pass

    # 2. SCHOOL TYPE SEARCH (Public/Private)
    if not expert_found and any(w in msg_low for w in ["publique", "public", "privé", "privee", "prive"]):
        is_public = any(w in msg_low for w in ["public", "publique"])
        try:
            res = safe_query(f"detail_ecole(ID, Name, _, TypeFee)")
            if res:
                found = []
                for r in res:
                    tfee = str(r['TypeFee']).lower()
                    is_sch_pub = "public" in tfee or "gratuit" in tfee
                    
                    if is_public and is_sch_pub:
                        found.append(clean_text(r['Name']))
                    elif not is_public and not is_sch_pub:
                        found.append(clean_text(r['Name']))
                
                if found:
                    stype_label = "Publics" if is_public else "Privés"
                    response_text = f"🏛️ **Établissements {stype_label} répertoriés :**\n"
                    for s in sorted(list(set(found)))[:10]:
                        response_text += f"- {s}\n"
                    source_detected = "prolog_expert"
                    expert_found = True
        except: pass

    # 3. SPECIFIC SCHOOL DETAILS (Fees, Majors, Campus)
    # Guard: Skip expert block for greetings/small-talk even if sticky memory has an entity
    is_greeting = any(w in msg_low for w in ["bonjour", "salut", "hello", "hi", "bonsoir", "merci", "ok", "oui", "non", "salam", "cv", "ça va"])
    is_pure_greeting = is_greeting and not found_brute and not any(w in msg_low for w in ["frais", "info", "parle", "école", "ecole", "filière", "spécialité", "internat"])
    
    if not expert_found and not is_pure_greeting and (detected_intent in ["FINANCIALS", "CAMPUS_LIFE", "SCHOOL_MAJORS", "SALARY_INFO"] or current_entity):
        sid = normalize_school_id(current_entity) if current_entity else normalize_school_id(msg_low)
        if sid:
            sid_clean = sanitize_prolog(sid)
            factual_resp = f"🎓 **Informations Expertes : {sid.upper()}**\n\n"
            inner_hit = False
            
            try:
                is_general = any(w in msg_low for w in ["parle", "info", "tout", "détail", "detail", "c'est quoi"]) or detected_intent == "GENERAL_INFO"
                
                # 1. Definition (Always first if general, or if explicitly asked)
                if is_general or "c'est quoi" in msg_low:
                    res_d = safe_query(f"get_definition('{sid_clean}', Nom, Detail)")
                    if not res_d: res_d = safe_query(f"get_definition('{sid_clean.upper()}', Nom, Detail)")
                    
                    if res_d: 
                        factual_resp += f"ℹ️ **Infos :** {clean_text(res_d[0]['Nom'])}. {clean_text(res_d[0]['Detail'])}\n"
                        inner_hit = True
                    else:
                        res_d2 = safe_query(f"definition('{sid_clean}', Def)")
                        if not res_d2: res_d2 = safe_query(f"definition('{sid_clean.upper()}', Def)")
                        if res_d2:
                            factual_resp += f"ℹ️ **Infos :** {clean_text(res_d2[0]['Def'])}\n"
                            inner_hit = True

                # 2. Financials
                if is_general or "frais" in msg_low or "prix" in msg_low or detected_intent == "FINANCIALS":
                    res = safe_query(f"detail_ecole('{sid_clean}', _, _, F)")
                    if res: factual_resp += f"💰 **Frais :** {clean_text(res[0]['F'])}\n"; inner_hit = True
                    elif sid.lower() in ["ensa", "encg", "fst", "est", "ests", "ensias", "emi", "ehtp", "inpt", "ensam"]:
                        factual_resp += "💰 **Frais :** Gratuit (Établissement Public)\n"; inner_hit = True
                
                # 3. Campus
                if is_general or any(w in msg_low for w in ["vie", "internat", "clubs"]) or detected_intent == "CAMPUS_LIFE":
                    res_i = safe_query(f"internat('{sid_clean}', I)")
                    if res_i: factual_resp += f"🏠 **Internat :** {clean_text(res_i[0]['I'])}\n"; inner_hit = True
                
                # 4. Majors
                if is_general or "filière" in msg_low or "spécialité" in msg_low or detected_intent == "SCHOOL_MAJORS":
                    res = safe_query(f"filiere(_, _, Nom, '{sid_clean.upper()}', _, _)")
                    if res:
                        majors = sorted(list(set([clean_text(r['Nom']) for r in res])))
                        factual_resp += f"📚 **Spécialités :** {', '.join(majors[:5])}\n"; inner_hit = True
                
                # 5. Definition Fallback (Only if nothing matched at all)
                if not inner_hit:
                    res_d = safe_query(f"get_definition('{sid_clean}', Nom, Detail)")
                    if not res_d: res_d = safe_query(f"get_definition('{sid_clean.upper()}', Nom, Detail)")
                    if res_d: factual_resp += f"ℹ️ **Infos :** {clean_text(res_d[0]['Nom'])}. {clean_text(res_d[0]['Detail'])}\n"; inner_hit = True
                    else:
                        res_d2 = safe_query(f"definition('{sid_clean}', Def)")
                        if not res_d2: res_d2 = safe_query(f"definition('{sid_clean.upper()}', Def)")
                        if res_d2: factual_resp += f"ℹ️ **Infos :** {clean_text(res_d2[0]['Def'])}\n"; inner_hit = True

                if inner_hit:
                    response_text = factual_resp
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 4. ADVICE & STRATEGY (Non-Exclusive, flows into LLM)
    if not expert_found:
        if detected_intent == "BAC_INFO":
            # Extract Bac type
            bt = "PC" if "pc" in msg_low else ("SVT" if "svt" in msg_low else ("SM" if "sm" in msg_low else ("ECO" if "eco" in msg_low else None)))
            if bt:
                try:
                    res_d = safe_query(f"detail_bac('{bt}', Id, Av, Li, Co)")
                    if res_d: expert_context = f"CONSEILS BAC {bt}:\n- Idéal: {clean_text(res_d[0]['Id'])}\n- Conseil: {clean_text(res_d[0]['Co'])}\n"
                except: pass
            else: expert_context = "CONSIGNE: Propose ton aide pour les bacs PC, SVT, SM ou ÉCONOMIE."

        elif detected_intent == "ORIENTATION_STRATEGY":
            match = re.search(r"\b(1\d|20|10)(\.[0-9]+)?\b", msg_low)
            grade = float(match.group()) if match else None
            if grade:
                try:
                    res = safe_query(f"strategie_profil({grade}, _, S)")
                    if res: expert_context = f"STRATÉGIE ({grade}/20): {clean_text(res[0]['S'])}"
                except: pass
            else: expert_context = "CONSIGNE: Demande la moyenne au bac pour une stratégie."

        elif detected_intent == "GENERAL_INFO" or any(w in msg_low for w in ["lmd", "bts", "dut"]):
            target = "LMD" if "lmd" in msg_low else ("BTS" if "bts" in msg_low else ("DUT" if "dut" in msg_low else None))
            if target:
                res = safe_query(f"get_definition('{target}', N, D)")
                if res: expert_context = f"DÉFINITION {target}: {clean_text(res[0]['N'])}. {clean_text(res[0]['D'])}"
        
        # If still empty, use a generic orientator prompt
        if not expert_context:
            expert_context = "INSTRUCTION: Tu es YAFI, expert en orientation au MAROC. Aide l'utilisateur à choisir une école ou un domaine."

    # --- PHASE 3: HYBRID ENGINE (PROLOG + RAG) ---
    print(f"[PHASE 3] Hybrid Engine Query (Determinism check)")
    
    # CRITICAL FIX: If response_text is ALREADY set by an expert handler (Score, Bourse, etc.)
    # and it is NOT a "CONSIGNE" or recommendation that needs warmth, return it immediately.
    # This prevents the LLM from overwriting deterministic facts with hallucinations.
    needs_llm_warmth = any(w in expert_context for w in ["ORIENTATION", "STRATÉGIE", "CONSEIL"])
    has_deterministic_resp = response_text and not needs_llm_warmth
    
    if (not response_text or expert_context) and not has_deterministic_resp:
        try:
            rag_context = ""
            # On ne tente le RAG que si le système expert n'a pas été suffisant
            if not expert_context and not response_text:
                rag_result = rag_system.generate_response(user_message, session_id=current_session_id, profile=profile)
                rag_context = rag_result.get("response", "")
            
            # --- PHASE 3: AUGMENTED GENERATION (The Hybrid Final Step) ---
            final_output_context = (expert_context or "") + (rag_context or "")
            
            # LEVEL 2 FIX: Proactively sync THE TOPIC to memory BEFORE generating 
            # (prevents amnesia during streaming or concurrent messages)
            if current_entity:
                user_memory.update(current_session_id, {"last_topic": current_entity})
                
            # SAFE PRINT FOR WINDOWS
            try:
                print(f"DEBUG: Combined Hybrid Context:\n{final_output_context}")
            except UnicodeEncodeError:
                print(f"DEBUG: Combined Hybrid Context (ASCII):\n{final_output_context.encode('ascii', 'ignore').decode('ascii')}")
            
            if should_stream:
                print("  Streaming Hybrid response...")
                def hybrid_stream():
                    yield json.dumps({"type": "start"}) + "\n"
                    full_resp = ""
                    # --- PHASE 4: LLM GENERATION ---
                    print(f"[PHASE 4] LLM Generation (Streaming)")
                    for chunk in llm_engine.ask_stream(user_message, expert_context=final_output_context, user_profile=profile):
                        full_resp += chunk
                        yield json.dumps({"token": chunk}) + "\n"
                    
                    # Sauvegarde finale en fin de stream
                    user_memory.add_message(current_session_id, 'user', user_message)
                    user_memory.add_message(current_session_id, 'assistant', full_resp)
                    elapsed = round((time.time() - start_time) * 1000)
                    yield json.dumps({
                        "type": "end", 
                        "full_response": full_resp, 
                        "response_time_ms": elapsed, 
                        "entities": entities,
                        "source": "hybrid_expert_llm" if expert_context else "ollama_advanced"
                    }) + "\n"
                
                return Response(hybrid_stream(), mimetype='application/x-ndjson')
            else:
                # Mode non-streaming
                response_text = llm_engine.ask(user_message, expert_context=final_output_context, user_profile=profile)
                source_detected = "hybrid_expert_llm"
        except Exception as e:
            print(f"  Hybrid Error: {e}")
            if not response_text:
                response_text = "Désolé, je rencontre une petite difficulté technique. Peux-tu reformuler ta question ?"
    
    # --- PHASE 6: FINALISATION & PERSISTANCE ---
    print(f"[PHASE 6] Finalisation & Persistence")
    if not response_text:
        response_text = "Bonjour ! Comment puis-je vous orienter aujourd'hui ?"

    user_memory.add_message(current_session_id, 'user', user_message)
    user_memory.add_message(current_session_id, 'assistant', response_text)
    
    elapsed = round((time.time() - start_time) * 1000)
    response_data = {
        "response": response_text,
        "response_time_ms": elapsed,
        "source": source_detected or "fallback",
        "entities": entities,
        "done": True
    }

    if should_stream:
        def stream_single():
            yield json.dumps(response_data) + "\n"
        return Response(stream_single(), mimetype='application/x-ndjson')
    
    return jsonify(response_data)

# --- TEST ENDPOINTS ---
@app.route('/test/components', methods=['GET'])
def test_components():
>>>>>>> 3257fc1 (final)
    status = {
        "ollama": "✓ Enabled" if is_ollama_available() else "✗ Disabled",
        "vector_search": "✓ Enabled" if (rag_system.vector_kb and rag_system.vector_kb.service) else "✗ Disabled",
        "prolog": "✓ Working" if prolog else "✗ Failed",
<<<<<<< HEAD
        "enhanced_rag": "✓ Ready" if rag_system else "✗ Failed",
    }
    return jsonify(status)

# ============================================================================
# HISTORY & MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get conversation history"""
    session_id = request.args.get('session_id', 'default')
    history = conversation_manager.get_history(session_id)
    return jsonify({"session_id": session_id, "message_count": len(history), "history": history})

@app.route('/chat/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    data = request.json
    session_id = data.get('session_id', 'default')
    conversation_manager.clear_session(session_id)
    return jsonify({"message": "Cleared", "session_id": session_id})

# ============================================================================
# EXPERT PROLOG ENDPOINTS (NEURO-SYMBOLIC INTEGRATION)
# ============================================================================

@app.route('/api/evaluate', methods=['POST'])
def evaluate_profile():
    """
    Advanced Prolog Expert Function:
    Calculates the 'Score d\'Orientation' based on Bac, Budget, and City.
    Expected JSON: {"bac": "PC", "budget": 20000, "ville": "Rabat", "ecole": "ENSA"}
    """
    data = request.json
    bac = data.get('bac', 'PC').upper()
    moyenne = data.get('moyenne', 14)
    budget = data.get('budget', 50000)
    ville = data.get('ville', 'Casablanca').capitalize()
    ecole = data.get('ecole', 'ENSA').upper()
    
    try:
        # Example: calculer_score_orientation('PC', 15, 30000, 'Rabat', 'ENSA', ScoreFinal).
        q = f"calculer_score_orientation('{bac}', {moyenne}, {budget}, '{ville}', '{ecole}', Score)"
        res = list(prolog.query(q))
        
        if res:
            score = res[0].get('Score')
            return jsonify({
                "status": "success", 
                "score": score,
                "message": f"Le score d'affinité pour {ecole} est de {score}% (Basé sur le Bac {bac}, moyenne {moyenne}, budget {budget}DH, et localisation {ville})."
            })
        else:
            return jsonify({"status": "no_match", "message": "Calcul impossible avec ces paramètres."})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║  YAFI Server v2 (Optimized - Ollama First) ║
    ║  Port: 5000                                ║
    ║  Ollama: %s                             ║
    ║  Vector Search: %s                     ║
    ╚════════════════════════════════════════════╝
    """ % (
        "✓ ENABLED" if is_ollama_available() else "✗ disabled",
        "✓ ENABLED" if (rag_system.vector_kb and rag_system.vector_kb.service) else "✗ disabled"
    ))
    print("\nAccess /test/components to verify setup ✓")
    app.run(port=5000, debug=True)
=======
    }
    return jsonify(status)

if __name__ == '__main__':
    print("YAFI Server v2.1 Hybrid - Port: 5000 [READY]")
    app.run(port=5000, debug=True)

>>>>>>> 3257fc1 (final)
