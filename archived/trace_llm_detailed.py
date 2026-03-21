#!/usr/bin/env python3
"""
🔍 YAFI LLM Trace Viewer
Affiche les traces détaillées du pipeline RAG + Ollama
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire backend au Python path
sys.path.insert(0, str(Path(__file__).parent))

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def print_section(text):
    print(f"\n{'─'*80}")
    print(f"  {text}")
    print(f"{'─'*80}\n")

def trace_question(question):
    """Trace complète d'une question"""
    
    print_header(f"🔍 TRACE DÉTAILLÉE - Question: {question}")
    
    # ════════════════════════════════════════════════════════════════════════
    # ÉTAPE 1: Recherche Vectorielle
    # ════════════════════════════════════════════════════════════════════════
    print_section("ÉTAPE 1️⃣ : RECHERCHE VECTORIELLE (FAISS)")
    
    try:
        from vector_knowledge import VectorKnowledge
        
        print(f"📥 Question reçue: '{question}'")
        print(f"⏳ Conversion en vecteur...")
        
        vk = VectorKnowledge()
        results = vk.search(question, top_k=3)
        
        print(f"✅ Recherche terminée")
        print(f"📊 {len(results)} documents trouvés\n")
        
        context = ""
        for i, (score, content) in enumerate(results, 1):
            print(f"   Document {i}:")
            print(f"   ┌─ Score de pertinence: {score:.4f}")
            print(f"   ├─ Contenu: {content[:100]}...")
            print(f"   └─ Longueur: {len(content)} caractères\n")
            context += content + "\n"
        
    except Exception as e:
        print(f"❌ ERREUR recherche vectorielle: {e}")
        return
    
    # ════════════════════════════════════════════════════════════════════════
    # ÉTAPE 2: Construction du Prompt
    # ════════════════════════════════════════════════════════════════════════
    print_section("ÉTAPE 2️⃣ : CONSTRUCTION DU PROMPT")
    
    try:
        from prompt_engine import PromptEngine
        
        prompt_engine = PromptEngine()
        
        # Construire le prompt avec le contexte
        system_prompt = """Tu es un assistant intelligent spécialisé dans l'orientation scolaire.
Aide les étudiants avec des conseils personnalisés basés sur la base de données disponible.
Réponds toujours en français, de manière claire et structurée."""
        
        full_prompt = f"""CONTEXTE (Base de données):
{context}

QUESTION: {question}

RÉPONSE:"""
        
        print(f"📝 Système Prompt:")
        print(f"   {system_prompt[:150]}...\n")
        
        print(f"📄 Prompt complet envoyé à Ollama:")
        print(f"┌─ LONGUEUR: {len(full_prompt)} caractères")
        print(f"├─ CONTEXTE: {len(context)} caractères")
        print(f"├─ QUESTION: {len(question)} caractères")
        print(f"└─ CONTENU:\n")
        
        # Afficher le prompt avec formatage
        prompt_lines = full_prompt.split('\n')
        for i, line in enumerate(prompt_lines[:15]):
            print(f"   {i+1:2}: {line}")
        if len(prompt_lines) > 15:
            print(f"   ... ({len(prompt_lines)-15} lignes supplémentaires)")
        
    except Exception as e:
        print(f"❌ ERREUR construction prompt: {e}")
        return
    
    # ════════════════════════════════════════════════════════════════════════
    # ÉTAPE 3: Appel Ollama
    # ════════════════════════════════════════════════════════════════════════
    print_section("ÉTAPE 3️⃣ : APPEL À OLLAMA LLM")
    
    try:
        import requests
        import time
        
        ollama_url = "http://localhost:11435/api/generate"
        
        print(f"🤖 Paramètres Ollama:")
        print(f"   ├─ URL: {ollama_url}")
        print(f"   ├─ Modèle: llama3.2:1b")
        print(f"   ├─ Température: 0.3 (déterministe)")
        print(f"   ├─ Mode: generate (streaming désactivé)")
        print(f"   └─ Timeout: 60 secondes\n")
        
        print(f"⏳ Envoi du prompt à Ollama...")
        print(f"⌛ Attente de la réponse (peut prendre 10-30 secondes)...\n")
        
        start_time = time.time()
        
        response = requests.post(
            ollama_url,
            json={
                "model": "llama3.2:1b",
                "prompt": full_prompt,
                "stream": False,
                "temperature": 0.3
            },
            timeout=120
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            ollama_response = data.get('response', '').strip()
            
            print(f"✅ RÉPONSE REÇUE DE OLLAMA")
            print(f"   ├─ Statut HTTP: {response.status_code}")
            print(f"   ├─ Temps: {elapsed:.1f} secondes")
            print(f"   ├─ Longueur: {len(ollama_response)} caractères")
            print(f"   └─ Modèle utilisé: llama3.2:1b\n")
            
            print(f"💬 CONTENU DE LA RÉPONSE OLLAMA:")
            print(f"┌{'─'*78}┐")
            for line in ollama_response.split('\n'):
                print(f"│ {line:<76} │")
            print(f"└{'─'*78}┘\n")
            
        else:
            print(f"❌ ERREUR: Code HTTP {response.status_code}")
            print(f"   Réponse: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ ERREUR appel Ollama: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ════════════════════════════════════════════════════════════════════════
    # ÉTAPE 4: Formatage de la réponse finale
    # ════════════════════════════════════════════════════════════════════════
    print_section("ÉTAPE 4️⃣ : RÉPONSE FINALE DU CHATBOT")
    
    try:
        from response_builder import ResponseBuilder
        
        response_builder = ResponseBuilder()
        
        # Construire la réponse finale avec sources
        final_response = response_builder.build_response(
            answer=ollama_response,
            context_sources=results
        )
        
        print(f"✅ RÉPONSE FINALE FORMATÉE:\n")
        print(f"┌{'─'*78}┐")
        for line in final_response.split('\n'):
            print(f"│ {line:<76} │")
        print(f"└{'─'*78}┘\n")
        
    except Exception as e:
        print(f"ℹ️  Pas de formatage supplémentaire (module response_builder: {e})")
        print(f"\n📋 RÉPONSE BRUTE DE OLLAMA:")
        print(f"┌{'─'*78}┐")
        for line in ollama_response.split('\n'):
            print(f"│ {line:<76} │")
        print(f"└{'─'*78}┘\n")
    
    # ════════════════════════════════════════════════════════════════════════
    # RÉSUMÉ
    # ════════════════════════════════════════════════════════════════════════
    print_section("📊 RÉSUMÉ DU PIPELINE")
    
    print(f"✅ Étapes complétées:")
    print(f"   1. ✅ Recherche vectorielle (FAISS) - {len(results)} documents")
    print(f"   2. ✅ Construction du prompt - {len(full_prompt)} caractères")
    print(f"   3. ✅ Appel Ollama - {elapsed:.1f}s")
    print(f"   4. ✅ Formatage réponse - {len(ollama_response)} caractères\n")
    
    print(f"🎯 Pipeline complet: QUESTION → FAISS → OLLAMA → RÉPONSE")
    print(f"✨ Ollama a bien aidé à générer une réponse intelligente!\n")

def main():
    print_header("🔍 YAFI LLM TRACE VIEWER")
    print("Affiche les traces détaillées du pipeline RAG + Ollama\n")
    
    # Questions de test
    questions = [
        "Quelle est l'importance de bien choisir son orientation scolaire?",
        "Quelles sont les meilleures écoles en informatique?",
        "Comment choisir entre sciences et lettres?"
    ]
    
    print("📋 Questions disponibles:\n")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q}")
    
    print("\n")
    choice = input("Quelle question tester? (1-3): ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(questions):
            trace_question(questions[idx])
        else:
            print("❌ Numéro invalide")
    except ValueError:
        print("❌ Entrée invalide")

if __name__ == "__main__":
    main()
