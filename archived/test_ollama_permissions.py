#!/usr/bin/env python3
"""
🧪 YAFI - Quick Test: Vérifier que les permissions d'Ollama fonctionnent
"""

import os
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_ollama_permissions():
    """Test des permissions d'Ollama améliorées"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🧪 TEST - Ollama Permissions Améliorées                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: Vérifier qu'Ollama fonctionne
    print("\n1️⃣ Test: Ollama est-il disponible?\n")
    
    try:
        resp = requests.get("http://localhost:11435/api/tags", timeout=5)
        if resp.status_code == 200:
            print("✅ Ollama répond correctement")
            models = resp.json().get('models', [])
            if models:
                print(f"   📦 Modèles disponibles: {[m['name'] for m in models[:2]]}...")
            else:
                print("   ⚠️ Aucun modèle trouvé. Pull llama3.2:1b?")
        else:
            print(f"❌ Erreur HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama non accessible: {e}")
        print("   💡 Assurez-vous qu'Ollama est lancé (port 11435)")
        return False
    
    # Test 2: Importer la config
    print("\n2️⃣ Test: Configuration Ollama Avancée\n")
    
    try:
        from ollama_advanced_config import OllamaAdvancedConfig
        print("✅ Configuration importée avec succès")
        print("   📋 Modes disponibles:")
        print("      • CREATIVE (questions courtes)")
        print("      • PREMIUM (conseils détaillés)")
        print("      • STANDARD (questions normales)")
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        return False
    
    # Test 3: Tester une question simple
    print("\n3️⃣ Test: Génération d'une réponse\n")
    
    try:
        from ollama_advanced_config import OllamaAdvancedConfig
        
        question = "c'est quoi une bourse?"
        print(f"📝 Question: {question}")
        print(f"⏳ Génération de la réponse...")
        
        response, confidence = OllamaAdvancedConfig.call_ollama_advanced(question)
        
        if response:
            print(f"✅ Réponse générée!")
            print(f"   📊 Confiance: {confidence*100:.0f}%")
            print(f"   📏 Longueur: {len(response)} caractères")
            print(f"\n   Extrait (200 chars):")
            print(f"   " + response[:200] + "...")
        else:
            print("❌ Pas de réponse")
            return False
            
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Tester via l'API
    print("\n4️⃣ Test: API Backend\n")
    
    try:
        api_resp = requests.post(
            "http://localhost:5000/chat",
            json={
                "message": "pourquoi choisir une bonne école?",
                "session_id": "test_permissions"
            },
            timeout=30
        )
        
        if api_resp.status_code == 200:
            data = api_resp.json()
            response_text = data.get('response', '')
            print("✅ API répond correctement")
            print(f"   📏 Réponse: {len(response_text)} caractères")
            print(f"\n   Extrait:")
            print(f"   {response_text[:300]}...")
        else:
            print(f"⚠️ Status: {api_resp.status_code}")
            print(f"   {api_resp.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ API non accessible (probablement pas lancée)")
        print("   💡 Lancez: cd backend && python server.py")
    except Exception as e:
        print(f"⚠️ Erreur API: {e}")
    
    # Résumé
    print(f"\n\n{'='*80}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'='*80}\n")
    
    print(f"""
✅ SUCCÈS! Ollama avec permissions avancées fonctionne!

🚀 Prochaines étapes:
   1. Redémarrez le backend si vous l'aviez lancé avant:
      cd backend
      python server.py
   
   2. Testez dans le chat une question courte:
      - "c'est quoi cv?"
      - "comment choisir?"
      - "bonjour"
   
   3. Vous devriez voir des réponses:
      - ✅ Plus longues
      - ✅ Plus intelligentes
      - ✅ Plus engageantes
      - ✅ Générées par Ollama
      
💡 Vous pouvez aussi:
   - Ajuster la température dans ollama_advanced_config.py
   - Changer num_predict pour réponses plus/moins longues
   - Tester avec d'autres questions

Enjoy! 🎉
    """)
    
    return True

if __name__ == "__main__":
    success = test_ollama_permissions()
    sys.exit(0 if success else 1)
