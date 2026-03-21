"""
YAFI Chatbot - OPTIMIZED SERVER v3
Focus: OLLAMA FIRST as PRIMARY response engine
Fallback to Prolog only if Ollama fails or doesn't have good data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog
import requests
import json

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

# Ollama config
OLLAMA_HOST = "http://localhost:11435"
OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_TIMEOUT = 30

def query_ollama(message: str, context: str = "") -> str:
    """Query Ollama for intelligent response"""
    try:
        prompt = f"{context}\n\nUser: {message}\n\nAssistant:"
        
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
            },
            timeout=OLLAMA_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            text = result.get("response", "").strip()
            return text if len(text) > 50 else ""
        return ""
    except Exception as e:
        print(f"Ollama error: {e}")
        return ""

def query_prolog(question: str) -> str:
    """Query Prolog as fallback"""
    try:
        # Attempt Prolog logic inference
        parts = question.lower().split()
        
        # Look for specific patterns  
        if any(word in question.lower() for word in ['pourquoi', 'why', 'raison']):
            result = list(prolog.query("solution_probleme(X, Y, Z)."))
            if result:
                return f"Ça pourrait être parce que: {result[0]}"
        
        # Default fall back response
        return ""
    except Exception as e:
        return ""

# ============================================================================
# MAIN CHAT ENDPOINT - OLLAMA FIRST
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
    """
    OPTIMIZED chat handler:
    1. Try OLLAMA FIRST (smart, intelligent)
    2. Fall back to Prolog if Ollama returns nothing
    """
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({"response": "Please provide a message"}), 400
    
    print(f"\n[Session {session_id}] Q: {user_message}")
    
    # STEP 1: Try Ollama FIRST
    print("→ Querying Ollama...")
    ollama_response = query_ollama(user_message)
    
    if ollama_response and len(ollama_response) > 100:
        print(f"✓ Got Ollama response ({len(ollama_response)} chars)")
        return jsonify({
            "response": ollama_response,
            "source": "OLLAMA",
            "session_id": session_id
        })
    
    # STEP 2: Fall back to Prolog
    print("→ Fallback to Prolog...")
    prolog_response = query_prolog(user_message)
    
    if prolog_response:
        print(f"✓ Got Prolog response ({len(prolog_response)} chars)")
        return jsonify({
            "response": prolog_response,
            "source": "PROLOG",
            "session_id": session_id
        })
    
    # STEP 3: Default response
    default_msg = "Je ne comprendre pas complètement votre question. Pouvez-vous la reformuler ou donner plus de détails?"
    print(f"→ Returning default response")
    return jsonify({
        "response": default_msg,
        "source": "DEFAULT",
        "session_id": session_id
    })

# ============================================================================
# STATUS ENDPOINT
# ============================================================================

@app.route('/', methods=['GET'])
def status():
    """Server status"""
    return jsonify({
        "status": "running",
        "version": "optimized-v3",
        "ollama": OLLAMA_HOST,
        "model": OLLAMA_MODEL
    })

@app.route('/status', methods=['GET'])
def full_status():
    """Full system status"""
    
    # Check Ollama
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        ollama_ok = r.status_code == 200
    except:
        pass
    
    return jsonify({
        "status": "running",
        "version": "optimized-v3",
        "port": 5001,
        "ollama": {
            "host": OLLAMA_HOST,
            "model": OLLAMA_MODEL,
            "available": ollama_ok
        },
        "prolog": "ready"
    })

# ============================================================================
# START
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("YAFI OPTIMIZED SERVER v3 - OLLAMA FIRST")
    print("="*70)
    print(f"Ollama host: {OLLAMA_HOST}")
    print(f"Ollama model: {OLLAMA_MODEL}")
    print(f"Listening on port 5001")
    print("="*70 + "\n")
    
    app.run(host='localhost', port=5001, debug=False)
