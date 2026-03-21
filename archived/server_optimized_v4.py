"""
YAFI Optimized Server V4 - WORKING VERSION
Uses Ollama with proper timeouts and fallback strategy
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog
import requests
import json
import threading
import time

app = Flask(__name__)
CORS(app)

# ============================================================================
# INITIALIZATION
# ============================================================================

prolog = Prolog()
try:
    prolog.consult('./knowledge_base_orientation')
    print("✓ Prolog knowledge base loaded")
except Exception as e:
    print(f"⚠️ Prolog failed: {e}")

# Ollama config - with extended timeout for slow model
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11435')
OLLAMA_MODEL = os.getenv('LLM_MODEL', 'llama3.2:1b')
OLLAMA_TIMEOUT = 120  # 2 minutes - llama3.2:1b is slow on CPU

def query_ollama_async(message: str, context: str, result_dict: dict, timeout: float = 120):
    """Query Ollama in a thread with timeout"""
    try:
        prompt = f"{context}\n\nQuestion: {message}\n\nAnswer:"
        
        # Try with streaming first (more reliable for slow models)
        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 150,  # Limit output length
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                result_dict['response'] = response.json().get("response", "").strip()
                result_dict['success'] = True
                return
        except requests.exceptions.Timeout:
            result_dict['error'] = 'timeout'
            return
        except Exception as e:
            result_dict['error'] = str(e)
            return
            
    except Exception as e:
        result_dict['error'] = str(e)

def query_ollama_with_timeout(message: str, context: str = "", max_wait: float = 8):
    """
    Query Ollama with timeout handling
    - Tries to get response within max_wait seconds
    - Falls back if it takes too long
    """
    result = {}
    thread = threading.Thread(
        target=query_ollama_async, 
        args=(message, context, result, 120),
        daemon=True
    )
    thread.start()
    thread.join(timeout=max_wait)
    
    if result.get('success'):
        return result.get('response', '')
    return ''

def query_prolog(question: str) -> str:
    """Query Prolog knowledge base"""
    try:
        # Basic pattern matching for Prolog
        lower_q = question.lower()
        
        # Look for known patterns
        for pattern, response_tuple in [
            ('python', ("solution(X) :- lang(python, X).","Prolog")),
            ('javascript', ("solution(X) :- lang(javascript, X).", "Prolog")),
            ('sommeil', ("solution(X) :- conseil_sante(sommeil, X).", "Prolog")),
            ('stress', ("solution(X) :- conseil_bien_etre(stress, X).", "Prolog")),
        ]:
            if pattern in lower_q:
                try:
                    query_str, source = response_tuple
                    results = list(prolog.query(query_str))
                    if results:
                        return f"(From knowledge base) {str(results[0]['X'])}"
                except:
                    pass
        
        return ""
    except Exception as e:
        return ""

# ============================================================================
# MAIN CHAT ENDPOINT - HYBRID APPROACH
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
    """
    Hybrid chat handler:
    1. Try Ollama with 20s timeout (fallback if too slow)
    2. Try Prolog 
    3. Return generic response
    """
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({"response": "Veuillez fournir un message."}), 400
    
    print(f"\n[Session {session_id}] Q: {user_message}")
    
    sources_tried = []
    
    # STEP 1: Try Ollama (with timeout safeguard)
    print("→ Trying Ollama (20s max)...")
    ollama_response = query_ollama_with_timeout(user_message, max_wait=20)
    
    if ollama_response and len(ollama_response) > 80:
        print(f"✓ Got Ollama response ({len(ollama_response)} chars)")
        return jsonify({
            "response": ollama_response,
            "source": "OLLAMA",
            "session_id": session_id
        })
    
    sources_tried.append("Ollama")
    
    # STEP 2: Try Prolog
    print("→ Trying Prolog...")
    prolog_response = query_prolog(user_message)
    
    if prolog_response:
        print(f"✓ Got Prolog response ({len(prolog_response)} chars)")
        return jsonify({
            "response": prolog_response,
            "source": "PROLOG",
            "session_id": session_id
        })
    
    sources_tried.append("Prolog")
    
    # STEP 3: Return fallback
    print(f"→ All sources exhausted, returning fallback")
    
    fallback_responses = [
        "Je ne suis pas certain de la réponse. Pouvez-vous reformuler votre question?",
        "C'est une question intéressante. Pourriez-vous donner plus de contexte?",
        "Je n'ai pas trouvé de réponse précise. Essayez une autre formulation.",
    ]
    
    fallback = fallback_responses[hash(user_message) % len(fallback_responses)]
    
    return jsonify({
        "response": fallback,
        "source": "FALLBACK",
        "session_id": session_id,
        "sources_tried": sources_tried
    })

# ============================================================================
# STATUS ENDPOINT
# ============================================================================

@app.route('/', methods=['GET'])
def status():
    """Server status"""
    # Check Ollama
    ollama_available = False
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        ollama_available = r.status_code == 200
    except:
        pass
    
    return jsonify({
        "status": "running",
        "version": "optimized-v4",
        "port": 5001,
        "ollama": {
            "available": ollama_available,
            "host": OLLAMA_HOST,
            "model": OLLAMA_MODEL
        }
    })

# ============================================================================
# START
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("YAFI OPTIMIZED SERVER V4 - HYBRID APPROACH")
    print("="*70)
    print(f"Ollama host: {OLLAMA_HOST}")
    print(f"Ollama model: {OLLAMA_MODEL}")
    print(f"Ollama timeout: 120s (with 20s user timeout)")
    print(f"Listening on port 5001")
    print("="*70 + "\n")
    
    app.run(host='localhost', port=5001, debug=False)
