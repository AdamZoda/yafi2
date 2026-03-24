
import os

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server_optimized.py'

# 1. Read existing content
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 2. Add KNOWN_ENTITIES and Helpers if missing
helper_code = """
# --- AXE 5 HELPERS ---
KNOWN_ENTITIES = [
    "emsi", "uir", "um6p", "ensa", "encg", "fst", "ensias", "iscae", "uic", "fmp",
    "ensam", "ensck", "isss", "ispits", "enam", "iav", "ispm", "itsat", "isic", "inau",
    "isadac", "esba", "inba", "insap", "aat", "isitt", "imsk", "iss", "issf", "irfcjs", "ena",
    "ofppt", "medecine", "pharmacie", "architecture", "minhaty",
    "casablanca", "rabat", "marrakech", "tanger", "agadir", "fes"
]

def normalize_school_id(name):
    name = name.lower().strip()
    mapping = {
        'emsi': 'emsi', 'uir': 'uir', 'um6p': 'um6p', 'ensa': 'ensa', 'encg': 'encg',
        'fst': 'fst', 'ensias': 'ensias', 'iscae': 'iscae', 'uic': 'uic', 'fmp': 'fmp',
        'ensam': 'ensam', 'enam': 'enam', 'iav': 'iav', 'ofppt': 'ofppt', 'medecine': 'medecine'
    }
    return mapping.get(name, name)

def get_upcoming_concours():
    # Placeholder or logic for upcoming concours
    return "📅 **Calendrier des Concours :**\\n- ENSA : Juillet\\n- ENCG (TAFEM) : Juillet\\n- Médecine (FMP) : Juillet"
"""

if "KNOWN_ENTITIES" not in text:
    text = text.replace("# ============================================================================", 
                        helper_code + "\n# ============================================================================", 1)

# 3. Completely Overhaul chat() function logic
# We'll replace handle from Phase 1 to the end of Phase 2 (RAG)

new_chat_logic = """
    # ========================================================================
    # PHASE 1: TRIVIAL & INTENT DETECTION (NEW PRIORITY)
    # ========================================================================
    
    msg_low = user_message.lower()
    user_message_normalized = normalize_text(user_message)
    current_entity = entities[0] if entities else None
    detected_intent = None

    # 1.1 Intent Classification
    if intent_classifier and intent_classifier.enabled:
        detected_intent = intent_classifier.classify(user_message_normalized, threshold=0.40)
        
        # BRUTE FORCE FALLBACK FOR COMPARISONS
        if detected_intent is None:
            if any(w in msg_low for w in ["comparer", "difference", " vs ", " entre "]):
                schools_found = [ent for ent in KNOWN_ENTITIES if ent in msg_low]
                if len(schools_found) >= 2:
                    detected_intent = "COMPARE_SCHOOLS"
                    print(f"🔥 BRUTE FORCE MATCH: {detected_intent}")

    # ========================================================================
    # PHASE 2: SPECIALIZED INTENT HANDLERS (PRIORITY)
    # ========================================================================

    # 2.1 TRIVIALS (Match immediately)
    if any(kw in msg_low for kw in ['yafi', 'y.a.f.i']):
        return jsonify({"response": "✨ **YAFI** est l'acronyme de notre Intelligence d'Orientation ! Cabinet d'orientation 2.0. 🎓"})
    
    elif msg_low in ['merci', 'ok', 'oui']:
        return jsonify({"response": "Je t'en prie ! D'autres questions ? ✨"})

    # 2.2 INTENT HANDLERS (Axe 5)
    if detected_intent == "COMPARE_SCHOOLS":
        schools_in_msg = [ent for ent in KNOWN_ENTITIES if ent in msg_low]
        if len(schools_in_msg) >= 2:
            s1, s2 = schools_in_msg[0], schools_in_msg[1]
            def fetch_school_data(name):
                sid = normalize_school_id(name)
                res_s = list(prolog.query(f"average_salary('{sid}', S)"))
                res_r = list(prolog.query(f"employment_rate('{sid}', R)"))
                res_c = list(prolog.query(f"localisation('{sid}', C)"))
                return {
                    "salary": clean_text(res_s[0]['S']) if res_s else "N/A",
                    "rate": f"{int(float(res_r[0]['R'])*100)}%" if res_r else "N/A",
                    "city": clean_text(res_c[0]['C']) if res_c else "N/A"
                }
            d1, d2 = fetch_school_data(s1), fetch_school_data(s2)
            resp = ResponseBuilder.build_comparison_response(s1.upper(), d1, s2.upper(), d2) if ResponseBuilder else f"⚖️ {s1.upper()} vs {s2.upper()}"
            return jsonify({"response": resp})
        else:
            return jsonify({"response": "⚖️ Précisez deux écoles pour une comparaison statistique (ex: EMSI vs UIR)."})

    elif detected_intent == "SALARY_INFO":
        if current_entity:
            sid = normalize_school_id(current_entity)
            res_s = list(prolog.query(f"average_salary('{sid}', S)"))
            res_r = list(prolog.query(f"employment_rate('{sid}', R)"))
            if res_s or res_r:
                sal = clean_text(res_s[0]['S']) if res_s else "N/A"
                rate = f"{int(float(res_r[0]['R'])*100)}%" if res_r else "N/A"
                return jsonify({"response": f"📊 **Stats {current_entity.upper()}** : Salaire ~{sal} DH, Insertion ~{rate}."})

    elif detected_intent == "SCHOOL_FEES" or "budget" in msg_low or "prix" in msg_low:
        res = list(prolog.query("get_frais_scolarite(Ecole, Prix, Note)"))
        if current_entity:
            for r in res:
                if current_entity == clean_text(r['Ecole']).lower():
                    return jsonify({"response": f"💰 **Frais {clean_text(r['Ecole'])}** : {clean_text(r['Prix'])}\\n{clean_text(r['Note'])}"})
        return jsonify({"response": f"💰 **Frais (Exemples)** :\\n- EMSI: 35-45k DH/an\\n- UIR: 60-90k DH/an"})

    # ========================================================================
    # PHASE 3: OLLAMA ADVANCED (RAG FALLBACK)
    # ========================================================================

    if not detected_intent and is_ollama_available():
"""

# Apply the rewrite (surgical replacement)
import re
text = re.sub(r'# ========================================================================.*?# PHASE 2: OLLAMA ADVANCED', 
              new_chat_logic + '    # Phase 2: OLLAMA ADVANCED', text, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("server_optimized.py overhauled to Intent-First.")
