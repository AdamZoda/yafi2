"""
YAFI Chatbot - OPTIMIZED SERVER V2
Focus: Ollama FIRST, then Prolog/Hard-coded as FALLBACK
================================
PRIORITY ORDER:
1. Trivial questions (YAFI definition, thanks, etc) -> Return immediately
2. OLLAMA ADVANCED (Smart, context-aware, intelligent) -> TRY FIRST
3. Prolog + Hard-coded -> Fallback if Ollama has insufficient data

This solves: "Hard-coded responses were blocking Ollama!"
"""

import sys
import os
from dotenv import load_dotenv

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
from llm_engine import llm_engine
from enhanced_rag import rag_system
from intent_classifier import IntentClassifier
from entity_extractor import entity_extractor
import user_memory

app = Flask(__name__)
CORS(app)

# ============================================================================
# INITIALIZATION
# ============================================================================

prolog = Prolog()
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
    if isinstance(text, str):
        return text.replace("\\n", "\n").strip()
    return str(text)

def normalize_text(text):
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
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
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
    status = {
        "ollama": "✓ Enabled" if is_ollama_available() else "✗ Disabled",
        "vector_search": "✓ Enabled" if (rag_system.vector_kb and rag_system.vector_kb.service) else "✗ Disabled",
        "prolog": "✓ Working" if prolog else "✗ Failed",
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
