#!/usr/bin/env python3
"""
YAFI API Endpoints for Ollama Testing
Provides endpoints to test LLM, RAG, and health checks
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from llm_engine import llm_engine
from enhanced_rag import rag_system
from prompt_engine import YAFIPromptEngine

app = Flask(__name__)
CORS(app)

# ===== Health Check Endpoints =====

@app.route('/health', methods=['GET'])
def health():
    """Check system health"""
    return jsonify({
        "status": "ok",
        "components": rag_system.health_check()
    })


@app.route('/api/ollama/health', methods=['GET'])
def ollama_health():
    """Check Ollama availability"""
    health = llm_engine.health_check()
    return jsonify(health)


# ===== Testing Endpoints =====

@app.route('/api/test/ollama', methods=['POST'])
def test_ollama():
    """Test Ollama direct response"""
    from flask import request
    
    data = request.json or {}
    prompt = data.get('prompt', 'Bonjour! Tu es YAFI, assistant d\'orientation. Présente-toi en une phrase.')
    temperature = data.get('temperature', 0.3)
    
    try:
        response = llm_engine.ask(prompt, temperature=temperature)
        
        if response:
            return jsonify({
                "status": "success",
                "response": response,
                "model": llm_engine.model_name,
                "provider": llm_engine.provider_name
            })
        else:
            return jsonify({
                "status": "error",
                "error": "Ollama returned empty response",
                "suggestion": "Check if Ollama is running: ollama serve"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/test/rag', methods=['POST'])
def test_rag():
    """Test RAG + Ollama integration"""
    from flask import request
    
    data = request.json or {}
    query = data.get('query', "C'est quoi l'ENSA ?")
    session_id = data.get('session_id', 'test_session')
    temperature = data.get('temperature', 0.3)
    
    try:
        result = rag_system.generate_response(
            user_query=query,
            session_id=session_id,
            use_llm=True,
            temperature=temperature
        )
        
        return jsonify({
            "status": "success",
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/test/prompt', methods=['POST'])
def test_prompt():
    """Test prompt generation"""
    from flask import request
    
    data = request.json or {}
    query = data.get('query', "Parle-moi de la médecine au Maroc")
    
    try:
        # Mock search results
        mock_results = [
            {
                'text': "La médecine au Maroc est enseignée à la Faculté de Médecine et Pharmacie.",
                'metadata': {'category': 'Études', 'question': 'Médecine'},
                'score': 0.90
            }
        ]
        
        prompt = YAFIPromptEngine.build_prompt(
            query=query,
            search_results=mock_results,
            history=[]
        )
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "length": len(prompt)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/test/full', methods=['POST'])
def test_full():
    """Test full pipeline: query -> RAG -> Ollama -> response"""
    from flask import request
    
    data = request.json or {}
    query = data.get('query', "Quelle est la meilleure école pour l'informatique au Maroc ?")
    session_id = data.get('session_id', 'test_full')
    
    try:
        result = rag_system.generate_response(
            user_query=query,
            session_id=session_id,
            use_llm=True,
            temperature=0.3
        )
        
        return jsonify({
            "status": "success",
            "query": query,
            "response": result.get("response", ""),
            "confidence": result.get("confidence", 0),
            "sources": result.get("sources", []),
            "method": result.get("method", "unknown"),
            "error": result.get("error")
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


# ===== Information Endpoints =====

@app.route('/api/info/system', methods=['GET'])
def system_info():
    """Get system information"""
    return jsonify({
        "python": sys.version,
        "backend_dir": backend_dir,
        "llm_config": {
            "provider": llm_engine.provider_name,
            "model": llm_engine.model_name,
            "host": llm_engine.ollama_host,
            "enabled": llm_engine.enabled
        },
        "rag_config": {
            "vector_kb_available": rag_system.vector_kb is not None,
            "min_similarity": rag_system.min_similarity,
            "context_chunks": rag_system.context_chunks
        }
    })


@app.route('/api/info/models', methods=['GET'])
def available_models():
    """Get available Ollama models"""
    import requests
    
    try:
        response = requests.get(
            f"{llm_engine.ollama_host}/api/tags",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            return jsonify({
                "status": "success",
                "count": len(models),
                "models": [
                    {
                        "name": m.get('name'),
                        "size": m.get('size'),
                        "digest": m.get('digest')
                    }
                    for m in models
                ]
            })
        else:
            return jsonify({
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 YAFI Ollama Test Server")
    print("=" * 70)
    print("\n📍 Available Endpoints:")
    print("   GET  /health                    - System health check")
    print("   GET  /api/ollama/health         - Ollama health check")
    print("   POST /api/test/ollama           - Test Ollama directly")
    print("   POST /api/test/rag              - Test RAG + Ollama")
    print("   POST /api/test/prompt           - Test prompt generation")
    print("   POST /api/test/full             - Test full pipeline")
    print("   GET  /api/info/system           - System information")
    print("   GET  /api/info/models           - Available models")
    print("\n🧪 Example Requests:")
    print("   curl http://localhost:5001/health")
    print("   curl -X POST http://localhost:5001/api/test/ollama \\")
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"prompt": "Bonjour!"}\'')
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')
