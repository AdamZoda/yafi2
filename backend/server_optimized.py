"""
YAFI Chatbot - OPTIMIZED SERVER V2
--------------------------------
PRIORITY ORDER:
1. Trivial questions -> Return immediately
2. Specialized Intents (Prolog Benchmarking, Fees, etc) -> HIGH PRIORITY
3. Ollama Advanced (RAG) -> FALLBACK if no specific intent
4. Generic Fallback

"""

import sys
import os
from dotenv import load_dotenv
import json
import re
import random
import time
import threading
import unicodedata
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from pyswip import Prolog

# Custom Modules
from conversation_manager import conversation_manager
from llm_engine import llm_engine
# from enhanced_rag import rag_system
# from intent_classifier import IntentClassifier
from entity_extractor import entity_extractor
import user_memory

# Load environment
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
load_dotenv(os.path.join(root_dir, ".env"))
sys.path.insert(0, base_dir)

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,ngrok-skip-browser-warning'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# ============================================================================
# INITIALIZATION
# ============================================================================

prolog = Prolog()
prolog_lock = threading.Lock()
# Knowledge Base
prolog.consult(os.path.join(base_dir, "full_orientation_system.pl").replace('\\', '/'))

# Components (DISABLED FOR PERFORMANCE)
vector_kb = None
intent_classifier = None
rag_system = None

def is_ollama_available():
    return llm_engine.enabled and llm_engine.health_check()['available']

def safe_query(query_str):
    """Thread-safe wrapper for Prolog queries"""
    with prolog_lock:
        return list(prolog.query(query_str))

def clean_text(text):
    if isinstance(text, str):
        return text.replace("\\n", "\n").strip()
    return str(text)

def normalize_text(text):
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
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
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
    
    # Brute-force entity detection (Find ALL mentioned)
    found_entities = []
    for entity in KNOWN_ENTITIES:
        if entity in msg_low:
            found_entities.append(entity)
    
    # Prioritize 'ecole' over others if found
    if found_entities:
        current_entity = found_entities[0]
        print(f"DEBUG: Brute-force detected entities: {found_entities}")
        # Sync all to profile for later comparison
        profile = user_memory.update(current_session_id, {"found_entities": found_entities})
    
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
    if not detected_intent and any(w in msg_low for w in ["salaire", "débouché", "insertion", "taux", "salary"]):
        detected_intent = "SALARY_INFO"
    if not detected_intent and any(w in msg_low for w in ["seuil", "note minimale", "note de coupure", "admission"]):
        detected_intent = "ADMISSION_THRESHOLD"
    if not detected_intent and any(w in msg_low for w in ["minhaty", "cursussup", "dossier", "inscription", "procedure", "procédure"]):
        detected_intent = "PROCEDURES_INFO"
    if not detected_intent and any(w in msg_low for w in ["peut faire", "compatible", "est-ce que", "possible", "recommande", "conseil"]):
        detected_intent = "COMPATIBILITY_CHECK"
    
    if not detected_intent and any(w in msg_low for w in ["bac pc", "bac svt", "bac sm", "bac eco", "bac lettres", "bac technique"]):
        detected_intent = "BAC_INFO"
    if not detected_intent and any(w in msg_low for w in ["conseil", "stratégie", "strategie", "que faire"]):
        detected_intent = "ORIENTATION_STRATEGY"

    if not detected_intent and intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)
        
    # 2. Comparison Logic (High Priority if 2+ schools found)
    if not detected_intent or detected_intent == "CALCULATE_SCORE":
        if len(found_entities) >= 2 or any(w in msg_low for w in ["comparer", "difference", " vs ", " entre "]):
            detected_intent = "COMPARE_SCHOOLS"
            print(f"BRUTE FORCE MATCH: {detected_intent}")

    # 3. Single School Intent Fallback
    if not detected_intent and any(w in msg_low for w in ["ville", "où se trouve", "situe", "emplacement", "opportunité", "concurrence"]):
        detected_intent = "CITY_INFOS"

    if not detected_intent and intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)

    source_detected = "hybrid_expert_llm" if detected_intent else "ollama_advanced"
    # ========================================================================
    # PHASE 2: SPECIALIZED EXPERT ROUTING (DETERMINISTIC FIRST)
    # ========================================================================
    expert_context = ""
    expert_found = False

    # 1. GEOGRAPHY & CITY SEARCH (High Priority)
    if not expert_found and (detected_intent in ["CITY_INFOS", "WHERE_TO_STUDY"] or any(c in msg_low for c in ["casablanca", "rabat", "marrakech", "fes", "tanger", "agadir", "safi", "kenitra", "oujda", "settat", "meknes", "benguerir", "oujda", "kenitra"])):
        city_match = None
        for c in ["casablanca", "rabat", "marrakech", "fes", "tanger", "agadir", "safi", "kenitra", "oujda", "settat", "meknes", "benguerir", "tetouan", "nador"]:
            if c in msg_low: 
                city_match = c if c != "casabla" else "casablanca"
                break
        
        if city_match:
            try:
                city_prolog = city_match.capitalize()
                res_loc = safe_query(f"localisation(S, '{city_prolog}')")
                if res_loc:
                    schools = sorted(list(set([r['S'].upper() for r in res_loc])))
                    
                    # Filter by Public/Private if requested
                    is_req_pub = any(w in msg_low for w in ["public", "publique"])
                    is_req_priv = any(w in msg_low for w in ["privé", "privee", "prive"])
                    is_req_ing = any(w in msg_low for w in ["ingénierie", "ingenierie", "ingenieur", "ingénieur"])
                    
                    filtered = []
                    for s in schools:
                        if is_req_ing and not any(k in s.lower() for k in ["ensa", "ensam", "emi", "ehtp", "inpt", "ensias", "ingenieur", "ingenierie", "emsi", "uir"]): continue
                        
                        dt = safe_query(f"detail_ecole('{s.lower()}', _, _, TF)")
                        is_sch_pub = "public" in str(dt[0]['TF']).lower() or "gratuit" in str(dt[0]['TF']).lower() if dt else (s.lower() not in ["emsi", "uir", "uik", "supinfo", "hem", "esca"])
                        
                        if is_req_pub and not is_sch_pub: continue
                        if is_req_priv and is_sch_pub: continue
                        filtered.append(s)
                    
                    if filtered: schools = filtered
                    
                    response_text = f"📍 **Établissements à {city_prolog} :**\n"
                    for s in schools: response_text += f"- {s}\n"
                    
                    # Add stats
                    res_opp = safe_query(f"ville_opportunite('{city_match}', O)")
                    if res_opp: response_text += f"\n💡 **Opportunité :** {clean_text(res_opp[0]['O'])}\n"
                    
                    res_con = safe_query(f"ville_concurrence('{city_prolog}')")
                    if res_con: response_text += f"\n⚠️ **Concurrence :** TRÈS FORTE dans cette ville.\n"
                    
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

    # 2b. COMPARE SCHOOLS (Logical cross-referencing)
    if not expert_found and detected_intent == "COMPARE_SCHOOLS":
        schools_to_compare = found_entities if len(found_entities) >= 2 else [s for s in KNOWN_ENTITIES if s in msg_low]
        if schools_to_compare:
            expert_context = "COMPARAISON EXPERTE :\n"
            for s in schools_to_compare[:3]:
                res_d = safe_query(f"definition('{s}', D)")
                if not res_d: res_d = safe_query(f"definition('{s.upper()}', D)")
                if res_d:
                    expert_context += f"- {s.upper()} : {clean_text(res_d[0]['D'])}\n"
                
                res_f = safe_query(f"detail_ecole('{s}', _, _, F)")
                if res_f:
                    expert_context += f"  (Frais: {clean_text(res_f[0]['F'])})\n"
            
            expert_found = True
            source_detected = "prolog_expert"

    # 3. SCHOLARSHIPS / BOURSES
    if not expert_found and (detected_intent == "SCHOLARSHIPS" or any(w in msg_low for w in ["bourse", "financement"])):
        sid = normalize_school_id(current_entity) if current_entity else normalize_school_id(msg_low)
        if sid:
            sid_clean = sanitize_prolog(sid)
            try:
                res = safe_query(f"bourse_merite('{sid_clean}', Type, Cond)")
                if not res: res = safe_query(f"bourse_merite('{sid_clean.upper()}', Type, Cond)")
                if res:
                    response_text = f"🎓 **Bourses disponibles à {sid.upper()} :**\n\n"
                    for r in res:
                        response_text += f"- **{clean_text(r['Type'])}** : {clean_text(r['Cond'])}\n"
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 4. SALARY / SALAIRE / DEBOUCHES
    if not expert_found and (detected_intent == "SALARY_INFO" or any(w in msg_low for w in ["salaire", "salary", "débouché", "debouche"])):
        sid = normalize_school_id(current_entity) if current_entity else normalize_school_id(msg_low)
        if sid:
            sid_clean = sanitize_prolog(sid)
            try:
                res_sal = safe_query(f"average_salary('{sid_clean}', S)")
                if not res_sal: res_sal = safe_query(f"average_salary('{sid_clean.lower()}', S)")
                res_emp = safe_query(f"employment_rate('{sid_clean}', R)")
                if not res_emp: res_emp = safe_query(f"employment_rate('{sid_clean.lower()}', R)")
                
                if res_sal or res_emp:
                    response_text = f"💼 **Débouchés après {sid.upper()} :**\n\n"
                    if res_sal: response_text += f"- **Salaire moyen** : {res_sal[0]['S']} DH/mois\n"
                    if res_emp: response_text += f"- **Taux d'insertion** : {int(float(res_emp[0]['R']) * 100)}%\n"
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 5. ADMISSION THRESHOLDS (SEUILS)
    if not expert_found and detected_intent == "ADMISSION_THRESHOLD":
        sid = normalize_school_id(current_entity) if current_entity else normalize_school_id(msg_low)
        if sid:
            try:
                res = safe_query(f"seuil('{sid.upper()}', 2023, V)")
                if not res: res = safe_query(f"seuil('{sid}', 2023, V)")
                if res:
                    response_text = f"📊 **Seuil d'admission {sid.upper()} (2023) :** {res[0]['V']}/20\n\n*Note : Les seuils varient chaque année selon la demande.*"
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 6. PROCEDURES & ADMINISTRATIVE (Minhaty/CursusSup)
    if not expert_found and (detected_intent == "PROCEDURES_INFO" or any(w in msg_low for w in ["minhaty", "cursussup"])):
        target = "Minhaty" if "minhaty" in msg_low else ("CursusSup" if "cursussup" in msg_low else None)
        if not target and current_entity: target = current_entity
        if not target and "management" in msg_low: target = "isitt prive"
        
        if target:
            try:
                # Try specific procedure names first
                res = None
                if target == "Minhaty": res = safe_query("procedure('Dossier Minhaty', D)")
                
                if not res: res = safe_query(f"procedure('{sanitize_prolog(target)}', D)")
                if not res: res = safe_query(f"definition('{sanitize_prolog(target).upper()}', D)")
                if not res: res = safe_query(f"definition('{sanitize_prolog(target)}', D)")
                if not res: res = safe_query(f"definition('{target.capitalize()}', D)")
                
                if res:
                    response_text = f"📝 **Infos Procédure : {target.upper()}**\n\n{clean_text(res[0]['D'])}\n"
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 7. COMPATIBILITY & RECOMMENDATION (Bac vs Domaine)
    if not expert_found and (detected_intent == "COMPATIBILITY_CHECK" or any(w in msg_low for w in ["bac", "filiere", "filière"])):
        # Extract Bac and Domain
        bac_detected = (entities.get('bac') or profile.get('bac') or '').lower() if entities else None
        if not bac_detected:
            for b in ["pc", "svt", "sm", "eco", "lettres", "tech"]:
                if f"bac {b}" in msg_low or f" bac{b}" in msg_low: bac_detected = b; break
        
        domaine_detected = None
        for d in ["ingenierie", "medecine", "commerce", "informatique", "droit", "lettres", "science", "technique"]:
            if d in msg_low or (d == "ingenierie" and "ingenieur" in msg_low): domaine_detected = d; break
            
        if bac_detected and domaine_detected:
            try:
                # Specific Medicine Logic
                if domaine_detected == "medecine":
                    match = re.search(r"\b(1\d|20|10)(\.[0-9]+)?\b", msg_low)
                    grade = float(match.group()) if match else (profile.get('moyenne') if profile else None)
                    if grade:
                        res_m = safe_query(f"peut_faire_medecine('{bac_detected.upper()}', {grade}, R)")
                        if res_m:
                            response_text = f"🩺 **Diagnostic Médecine ({bac_detected.upper()}, {grade}/20) :**\n\n"
                            response_text += f"Verdict : {clean_text(res_m[0]['R'])}\n"
                            source_detected = "prolog_expert"
                            expert_found = True
                
                if not expert_found:
                    res = safe_query(f"check_compatibilite('{bac_detected}', {domaine_detected}, Statut, Msg)")
                    if res:
                        statut = str(res[0]['Statut']).upper()
                        emojis = {"EXCELLENT": "✅", "POSSIBLE": "⚠️", "IMPOSSIBLE": "❌", "INCONNU": "❓"}
                        response_text = f"🛡️ **Compatibilité {bac_detected.upper()} ➔ {domaine_detected.capitalize()}**\n\n"
                        response_text += f"Statut : {emojis.get(statut, '')} **{statut}**\n"
                        response_text += f"Conseil : {clean_text(res[0]['Msg'])}\n"
                        source_detected = "prolog_expert"
                        expert_found = True
            except: pass

    # 8. BAC DETAILS (Advantages/Limits/Ideals)
    if not expert_found and (detected_intent == "BAC_INFO" or any(w in msg_low for w in ["avantage", "limite", "ideal", "idéal"])):
        bac_target = (entities.get('bac') or profile.get('bac') or '').upper() if entities else None
        if not bac_target:
            for b in ["PC", "SVT", "SM", "ECO", "LITT", "TECH"]:
                if f"bac {b.lower()}" in msg_low: bac_target = b; break
        
        if bac_target:
            try:
                res = safe_query(f"detail_bac('{bac_target}', Ideales, Avantages, Limites, Conseil)")
                if res:
                    response_text = f"🎓 **Analyse Bac {bac_target} :**\n\n"
                    response_text += f"✨ **Filières Idéales** : {clean_text(res[0]['Ideales'])}\n"
                    response_text += f"✅ **Avantages** : {clean_text(res[0]['Avantages'])}\n"
                    response_text += f"⚠️ **Limites** : {clean_text(res[0]['Limites'])}\n"
                    response_text += f"💡 **Conseil** : {clean_text(res[0]['Conseil'])}\n"
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 9. SPECIFIC SCHOOL DETAILS (Fees, Majors, Campus)
    is_greeting = any(w in msg_low for w in ["bonjour", "salut", "hello", "hi", "bonsoir", "merci", "ok", "oui", "non", "salam", "cv", "ça va"])
    is_pure_greeting = is_greeting and not found_entities and not any(w in msg_low for w in ["frais", "info", "parle", "école", "ecole", "filière", "spécialité", "internat"])
    
    if not expert_found and not is_pure_greeting and (detected_intent in ["FINANCIALS", "CAMPUS_LIFE", "SCHOOL_MAJORS", "SALARY_INFO"] or current_entity):
        sid = normalize_school_id(current_entity) if current_entity else normalize_school_id(msg_low)
        if sid:
            sid_clean = sanitize_prolog(sid)
            res_d = None
            factual_resp = f"🎓 **Informations Expertes : {sid.upper()}**\n\n"
            inner_hit = False
            
            try:
                is_general = any(w in msg_low for w in ["parle", "info", "tout", "détail", "detail", "c'est quoi"]) or detected_intent == "GENERAL_INFO"
                
                # 1. Definition / Localization
                if is_general or any(w in msg_low for w in ["c'est quoi", "où", "ou se trouve", "emplacement", "lieu", "site"]):
                    res_d = safe_query(f"get_definition('{sid_clean}', Nom, Detail)")
                    if not res_d: res_d = safe_query(f"get_definition('{sid_clean.upper()}', Nom, Detail)")
                    if not res_d: res_d = safe_query(f"definition('{sid_clean}', Detail)")
                    if not res_d: res_d = safe_query(f"definition('{sid_clean.upper()}', Detail)")
                    if not res_d: res_d = safe_query(f"definition('{sid_clean.capitalize()}', Detail)")
                    
                    if res_d: 
                        name_val = res_d[0].get('Nom') or res_d[0].get('N') or sid_clean.upper()
                        factual_resp += f"ℹ️ **Infos :** {clean_text(name_val)}. {clean_text(res_d[0]['Detail']) if 'Detail' in res_d[0] else clean_text(res_d[0]['D'])}\n"
                        inner_hit = True
                    else:
                        res_d2 = safe_query(f"definition('{sid_clean}', Def)")
                        if not res_d2: res_d2 = safe_query(f"definition('{sid_clean.upper()}', Def)")
                        if not res_d2: res_d2 = safe_query(f"definition('{sid_clean.capitalize()}', Def)")
                        if res_d2:
                            factual_resp += f"ℹ️ **Infos :** {clean_text(res_d2[0]['Def'])}\n"
                            inner_hit = True
                    
                    # Add Geolocation if found
                    res_loc = safe_query(f"localisation('{sid_clean.upper()}', City)")
                    if not res_loc: res_loc = safe_query(f"localisation('{sid_clean}', City)")
                    if res_loc:
                        factual_resp += f"📍 **Localisation :** {clean_text(res_loc[0]['City'])}\n"
                        inner_hit = True

                # 2. Financials
                if is_general or "frais" in msg_low or "prix" in msg_low or detected_intent == "FINANCIALS":
                    res = safe_query(f"detail_ecole('{sid_clean}', _, _, F)")
                    if res: factual_resp += f"💰 **Frais :** {clean_text(res[0]['F'])}\n"; inner_hit = True
                    else:
                        res_f = safe_query(f"frais_scolarite('{sid_clean}', M, N)")
                        if not res_f: res_f = safe_query(f"frais_scolarite('{sid_clean.lower()}', M)")
                        if res_f:
                            m = res_f[0].get('M') or res_f[0].get('MoutantAnnuel')
                            factual_resp += f"💰 **Frais :** {m} DH/an (estimation)\n"; inner_hit = True
                        
                    if not inner_hit and sid.lower() in ["ensa", "encg", "fst", "est", "ests", "ensias", "emi", "ehtp", "inpt", "ensam"]:
                        factual_resp += "💰 **Frais :** Gratuit (Établissement Public)\n"; inner_hit = True
                
                # 3. Campus Life (Internat, Clubs, Cantine)
                if is_general or any(w in msg_low for w in ["vie", "internat", "clubs", "cantine", "manger"]) or detected_intent == "CAMPUS_LIFE":
                    res_i = safe_query(f"internat('{sid_clean}', I)")
                    if res_i: factual_resp += f"🏠 **Internat :** {clean_text(res_i[0]['I'])}\n"; inner_hit = True
                    
                    res_c = safe_query(f"clubs('{sid_clean}', C)")
                    if not res_c: res_c = safe_query(f"clubs('{sid_clean.lower()}', C)")
                    if res_c: factual_resp += f"🎭 **Clubs :** {clean_text(res_c[0]['C'])}\n"; inner_hit = True
                    
                    res_can = safe_query(f"cantine('{sid_clean}', Ca)")
                    if not res_can: res_can = safe_query(f"cantine('{sid_clean.lower()}', Ca)")
                    if res_can: factual_resp += f"🍴 **Cantine :** {clean_text(res_can[0]['Ca'])}\n"; inner_hit = True
                
                # 4. Majors
                if is_general or "filière" in msg_low or "spécialité" in msg_low or detected_intent == "SCHOOL_MAJORS":
                    res = safe_query(f"filiere(_, _, Nom, '{sid_clean.upper()}', _, _)")
                    if res:
                        majors = sorted(list(set([clean_text(r['Nom']) for r in res])))
                        factual_resp += f"📚 **Spécialités :** {', '.join(majors[:5])}\n"; inner_hit = True
                
                if inner_hit:
                    response_text = factual_resp
                    source_detected = "prolog_expert"
                    expert_found = True
            except: pass

    # 4. ADVICE & STRATEGY
    if not expert_found:
        if detected_intent == "BAC_INFO":
            bt = "PC" if "pc" in msg_low else ("SVT" if "svt" in msg_low else ("SM" if "sm" in msg_low else ("ECO" if "eco" in msg_low else None)))
            if bt:
                try:
                    res_d = safe_query(f"detail_bac('{bt}', Id, Av, Li, Co)")
                    if res_d: expert_context = f"CONSEILS BAC {bt}:\n- Idéal: {clean_text(res_d[0]['Id'])}\n- Conseil: {clean_text(res_d[0]['Co'])}\n"
                except: pass
            else: expert_context = "CONSIGNE: Propose ton aide pour les bacs PC, SVT, SM ou ÉCONOMIE."

        elif detected_intent == "ORIENTATION_STRATEGY" or "conseil" in msg_low:
            match = re.search(r"\b(1\d|20|10)(\.[0-9]+)?\b", msg_low)
            grade = float(match.group()) if match else (profile.get('moyenne') if profile else None)
            bac = (entities.get('bac') or profile.get('bac') or '_') if entities else '_'
            
            if grade:
                try:
                    res = safe_query(f"strategie_profil({grade}, '{sanitize_prolog(bac)}', S)")
                    if res: expert_context = f"STRATÉGIE ({grade}/20, Bac {bac}): {clean_text(res[0]['S'])}"
                except: pass
            else: expert_context = "CONSIGNE: Demande la moyenne au bac pour une stratégie précise."

        elif detected_intent == "GENERAL_INFO" or any(w in msg_low for w in ["lmd", "bts", "dut", "data scientist", "informatique", "génie civil", "architecture"]):
            target = "LMD" if "lmd" in msg_low else ("BTS" if "bts" in msg_low else ("DUT" if "dut" in msg_low else None))
            if not target:
                if "data scientist" in msg_low or "informatique" in msg_low: target = "Génie Informatique"
                elif "génie civil" in msg_low: target = "Génie Civil"
                elif "architecture" in msg_low: target = "Architecture"

            if target:
                res = safe_query(f"definition('{target}', D)")
                if not res: res = safe_query(f"definition('{target.upper()}', D)")
                if res: expert_context = f"DÉFINITION {target}: {clean_text(res[0]['D'])}"
                
                # Also list schools for this major if relevant
                res_s = safe_query(f"filiere(_, _, '{target}', S, _, _)")
                if not res_s: res_s = safe_query(f"filiere(_, _, _, S, '{target}', _)")
                if res_s:
                    schools = list(set([str(r['S']).upper() for r in res_s]))[:5]
                    expert_context += f"\nÉtablissements proposant cette filière: {', '.join(schools)}"
        
        elif any(w in msg_low for w in ["prive", "privé", "public", "publique"]) and any(w in msg_low for w in ["avantage", "limite", "différence", "comparer", "vs"]):
             try:
                 res_pub = safe_query("info_type(public_regule, D)")
                 res_priv = safe_query("info_type(prive, D)")
                 if res_pub and res_priv:
                     expert_context = f"COMPARAISON PUBLIC/PRIVÉ :\n- Public : {clean_text(res_pub[0]['D'])}\n- Privé : {clean_text(res_priv[0]['D'])}"
             except: pass
        
        elif not expert_found and re.search(r"(\d{4,6})", msg_low) and any(w in msg_low for w in ["budget", "frais", "prix", "dh", "payant", "moins de"]):
            budget_match = re.search(r"(\d{4,6})", msg_low)
            max_budget = int(budget_match.group(1))
            domain = "Génie Informatique" if "info" in msg_low else \
                     ("Architecture" if "archi" in msg_low else \
                     ("Management" if "management" in msg_low or "commerce" in msg_low else \
                     ("Ingénieur" if "ingénier" in msg_low or "ingenier" in msg_low else "Ingénierie")))
            try:
                res_b = safe_query(f"find_best_school_fuzzy('{sanitize_prolog(domain)}', {max_budget}, S)")
                if res_b:
                    schools = list(set([str(r['S']).upper() for r in res_b]))
                    expert_context = f"Établissements pour {domain} avec un budget maximum de {max_budget} DH/an :\n"
                    expert_context += f"- {', '.join(schools[:10])}\n"
                    expert_context += "CONSIGNE: Utilise un ton de 'Grand Frère' pour expliquer que les écoles publiques sont les meilleures options budget-friendly."
            except: pass

        if not expert_context:
            expert_context = "INSTRUCTION: Tu es YAFI, expert en orientation au MAROC. Aide l'utilisateur à choisir une école ou un domaine."

    # 10. RED TEAMING & GUARDRAILS
    red_teaming_alert = False
    if not expert_found:
        bad_keywords = ["python", "script", "hacker", "pirater", "foot", "joueur", "cuisine", "recette", "sorbonne", "lyon", "paris", "astrologie", "zodiaque"]
        if any(w in msg_low for w in bad_keywords):
            red_teaming_alert = True
            if any(w in msg_low for w in ["lyon", "sorbonne", "paris", "france"]):
                expert_context = "CONSIGNE: Tu es YAFI, expert uniquement pour le MAROC. Réponds poliment que tu ne couvres pas les études en France ou à l'étranger."
            elif any(w in msg_low for w in ["python", "script", "hacker", "pirater", "recette", "cuisine"]):
                expert_context = "CONSIGNE: Tu es un conseiller en orientation, pas un assistant technique ou culinaire. Refuse poliment de sortir de ton rôle."
            else:
                expert_context = "CONSIGNE: Tu es YAFI, conseiller expert d'orientation scolaire au Maroc. Recadre poliment l'utilisateur sur le domaine académique."

    # --- PHASE 3: HYBRID ENGINE (HUMANIZATION) ---
    # Merge response_text (deterministic) and expert_context (advisory) into a single Expert Knowledge packet
    expert_knowledge = (response_text or "") + "\n" + (expert_context or "")
    
    # We ALWAYS pass through the LLM for "Humanization" unless it's a very specific debugging case
    try:
        rag_context = ""
        if not expert_knowledge.strip():
            # semantic RAG disabled for speed, using LLM general knowledge
            rag_context = ""
        
        final_prompt_context = expert_knowledge + "\n" + rag_context
        
        # Build the Humanization System Prompt (v2.6 Professional)
        system_prompt = f"""Tu es YAFI, le système expert d'orientation scolaire au MAROC.
CONSIGNE : Synthétise et humanise les 'DONNÉES EXPERTES' ci-dessous pour répondre de manière professionnelle et encourageante.
RÈGLES :
1. Ne change JAMAIS les faits (seuils, villes, frais, spécialités).
2. Utilise un ton de 'Conseiller Expert' (précis et bienveillant).
3. Sois direct et synthétique. Utilise des listes à puces.
4. Si l'information est absente, admets-le poliment au lieu d'inventer.

DONNÉES EXPERTES :
{final_prompt_context}
"""
        
        if current_entity:
            user_memory.update(current_session_id, {"last_topic": current_entity})
            
        if should_stream:
            # Re-wrap in the dynamic engine
            def humanized_stream():
                # Signal immédiat pour "réveiller" Vercel et éviter le timeout de 30s
                yield json.dumps({"token": ""}) + "\n"
                
                for chunk in llm_engine.ask_stream(user_message, expert_context=system_prompt):
                     yield chunk
            # Using application/x-ndjson (Newline Delimited JSON) which matches our api.ts parser
            return Response(stream_with_context(humanized_stream()), mimetype='application/x-ndjson')
        else:
            final_resp = llm_engine.ask(user_message, expert_context=system_prompt)
            return jsonify({"response": final_resp, "source": source_detected or "hybrid_axe"})
            
    except Exception as e:
        # Emergency Fallback to direct text if LLM fails
        return jsonify({"response": expert_knowledge or "Désolé, j'ai rencontré une petite erreur technique.", "source": "emergency_fallback"})

# ============================================================================
# TEST ENDPOINTS
# ============================================================================

# ============================================================================
# TEST ENDPOINTS
# ============================================================================

@app.route('/test/ollama', methods=['GET'])
def test_ollama():
    if not is_ollama_available():
        return jsonify({"status": "disabled", "message": "Ollama not initialized"}), 503
    try:
        test_response = rag_system.generate_response("Bonjour", use_llm=True)
        return jsonify({"status": "working", "response": test_response.get("response")})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/test/prolog', methods=['GET'])
def test_prolog():
    try:
        res = list(prolog.query("yafi_definition(X)"))
        return jsonify({"status": "working", "result": res[0] if res else "no_data"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/test/components', methods=['GET'])
def test_components():
    return jsonify({
        "ollama": is_ollama_available(),
        "prolog": True,
        "vector_kb": vector_kb is not None,
        "intent_classifier": intent_classifier is not None and intent_classifier.enabled
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "timestamp": time.time()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
