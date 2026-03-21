#!/usr/bin/env python3
"""
🔍 YAFI - Diagnostic Complet
Vérifie si le problème vient d'Ollama ou de la base de connaissances
"""

import os
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_section(text):
    print(f"\n{'─'*80}")
    print(f"  {text}")
    print(f"{'─'*80}\n")

def diagnose_response_source(question):
    """Diagnostiquer la source d'une réponse"""
    
    print_section(f"🔍 DIAGNOSTIC: '{question}'")
    
    # 1. Tester Ollama directement
    print("1️⃣  TEST OLLAMA DIRECT")
    print("─" * 40)
    
    try:
        ollama_url = os.environ.get('OLLAMA_HOST', 'http://localhost:11435')
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": f"Réponds brièvement: {question}",
                "stream": False,
                "temperature": 0.4,
                "num_predict": 200
            },
            timeout=30
        )
        
        if response.status_code == 200:
            ollama_resp = response.json().get('response', '')
            print(f"✅ Ollama répond: {len(ollama_resp)} chars")
            print(f"   Extrait: {ollama_resp[:150]}...")
        else:
            print(f"❌ Ollama erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ollama non accessible: {e}")
    
    # 2. Tester Recherche Vectorielle
    print("\n2️⃣  TEST RECHERCHE VECTORIELLE")
    print("─" * 40)
    
    try:
        from vector_knowledge import VectorKnowledge
        
        vk = VectorKnowledge()
        results = vk.search(question, top_k=3, threshold=0.35)
        
        if results:
            print(f"✅ Recherche vectorielle: {len(results)} résultats")
            for i, (score, content) in enumerate(results[:1], 1):
                print(f"   [{i}] Score: {score:.3f}")
                print(f"       {content[:100]}...")
        else:
            print(f"❌ Aucun résultat vectoriel")
            
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
    
    # 3. Tester API Backend
    print("\n3️⃣  TEST API BACKEND")
    print("─" * 40)
    
    try:
        response = requests.post(
            "http://localhost:5000/chat",
            json={
                "message": question,
                "session_id": "diag"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            print(f"✅ Backend répond: {len(answer)} chars")
            
            # Détecter la source
            if answer.startswith("C'est une excellente") or "template" in answer.lower():
                print(f"   ⚠️  SOURCE: Probablement HARD-CODED")
            elif len(answer) < 150:
                print(f"   ⚠️  SOURCE: Probablement PROLOG/hard-coded")
            else:
                print(f"   ✅ SOURCE: Probablement OLLAMA")
            
            print(f"\n   Réponse: {answer[:200]}...")
        else:
            print(f"❌ Backend erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Backend non accessible: {e}")

def main():
    print_header("🔍 DIAGNOSTIC - Source des Réponses")
    
    test_questions = [
        "c'est quoi cv?",
        "Quel domaine sera populaire dans 10 ans?",
        "Je suis nul en maths, que faire?",
        "bonjour",
        "Comment choisir mon orientation?"
    ]
    
    print("""
Ce diagnostic vérifie:
1. ✅ Est-ce qu'Ollama fonctionne?
2. ✅ Est-ce que la recherche vectorielle fonctionne?
3. ✅ Qu'est-ce que le backend retourne?
4. ✅ D'où vient la réponse (Ollama vs hard-coded)?
    """)
    
    for question in test_questions:
        diagnose_response_source(question)
    
    # RÉSUMÉ
    print_header("📊 RÉSUMÉ & RECOMMANDATIONS")
    
    print("""
🎯 DIAGNOSTIC COMPLET:

Si vous voyez:
✅ Ollama répond bien
✅ Recherche vectorielle trouve des résultats
❌ Mais backend retourne du hard-coded

ALORS LE PROBLÈME EST: Les réponses hard-coded ont priorité sur Ollama!

SOLUTION: Vérifier server.py et s'assurer que:
1. Les réponses hard-coded sont APRÈS Ollama
2. Ou: Les réponses hard-coded ne s'activent PAS

───────────────────────────────────────────────────

Si vous voyez:
❌ Ollama répond mal
❌ Recherche vectorielle peu de résultats
✅ Backend core OK

ALORS LE PROBLÈME EST: Configuration Ollama ou base de connaissances

SOLUTIONS:
1. Vérifier ollama_advanced_config.py
2. Augmenter temperature/tokens
3. Améliorer les données vectorielles

───────────────────────────────────────────────────

PROCHAINES ÉTAPES:
1. Lancez ce script: python diagnose_response_source.py
2. Notez les résultats
3. Je vais fixer le problème identifié
    """)

if __name__ == "__main__":
    main()
