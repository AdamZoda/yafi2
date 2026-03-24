
import os

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server_optimized.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    # Fix multi-line string in SCHOOL_FEES
    if "return jsonify({\"response\": f\"💰 **Frais" in line:
        line = line.replace('Prix\'])}', 'Prix\'])} \\n {clean_text(r[\'Note\'])}')
        # The next line in the file was the second half of this broken string
        skip_next = True 
        new_lines.append(line.strip() + '"})\n')
        continue

    if "return jsonify({\"response\": f\"💰 **Frais (Exemples)** :" in line:
        line = line.replace('Exemples)** :', 'Exemples)** : \\n - EMSI: 35-45k DH/an \\n - UIR: 60-90k DH/an')
        # The next two lines were parts of this broken string
        for _ in range(2):
            if i + 1 + _ < len(lines):
                # We skip the next 2 lines
                pass
        # Skip logic is a bit tricky here, let's just replace the whole block in new_lines
        new_lines.append(line.strip() + '"})\n')
        # We need to skip the next 2 lines manually in the loop
        # But wait, let's just use a simpler approach.
        continue
    
    # Clean up duplicated RAG entry
    if 'if not detected_intent and is_ollama_available():' in line:
        # Check if the next non-empty line is also an if
        next_idx = i + 1
        while next_idx < len(lines) and not lines[next_idx].strip():
            next_idx += 1
        if next_idx < len(lines) and 'if not response_text and is_ollama_available():' in lines[next_idx]:
            # Consolidate them
            new_lines.append('    if not detected_intent and not response_text and is_ollama_available():\n')
            # We will skip the next 'if' explicitly when we reach it
            continue

    if 'if not response_text and is_ollama_available():' in line and i > 100: # avoid the first one
        # This was the second one, we already consolidated it above
        # But we need to make sure we don't skip the first one by accident.
        # Actually, let's just skip this one.
        continue

    new_lines.append(line)

# Re-filter to skip the lines we wanted to skip
# Actually, the above logic is a bit messy. Let's just do a clean rewrite of the chat() function again with better string handling.

final_chat_logic = r'''
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
                    resp = f"💰 **Frais {clean_text(r['Ecole'])}** : {clean_text(r['Prix'])}\\n{clean_text(r['Note'])}"
                    return jsonify({"response": resp})
        resp = "💰 **Frais (Exemples)** :\\n- EMSI: 35-45k DH/an\\n- UIR: 60-90k DH/an"
        return jsonify({"response": resp})

    # ========================================================================
    # PHASE 3: OLLAMA ADVANCED (RAG FALLBACK)
    # ========================================================================

    response_text = None
    if not detected_intent and is_ollama_available():
'''

# Surgical replacement of the problematic block
import re
with open(filepath, 'r', encoding='utf-8') as f:
    full_text = f.read()

# We look for the start of chat() logic and the end of RAG entry
full_text = re.sub(r'# ========================================================================.*?if not response_text and is_ollama_available\(\):', 
                  final_chat_logic, full_text, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(full_text)

print("server_optimized.py cleaned and fixed.")
