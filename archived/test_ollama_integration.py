#!/usr/bin/env python3
"""
Test script for Ollama integration with YAFI system
Tests LLM engine, RAG search, and end-to-end response generation
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from llm_engine import llm_engine, OllamaProvider
from prompt_engine import YAFIPromptEngine
from vector_knowledge import VectorKnowledgeBase
from conversation_manager import conversation_manager

load_dotenv()

print("=" * 70)
print("🧪 YAFI Ollama Integration Test")
print("=" * 70)

# ===== Test 1: Basic LLM Connection =====
print("\n[TEST 1] Basic Ollama Connection")
print("-" * 70)
try:
    response = llm_engine.ask("Bonjour! Raconte-moi en une phrase qui tu es.")
    if response and len(response) > 5:
        print("✅ Ollama Response:")
        print(f"   {response[:150]}...")
    else:
        print("❌ Empty or short response from Ollama")
except Exception as e:
    print(f"❌ Error: {e}")

# ===== Test 2: Vector Knowledge Base =====
print("\n[TEST 2] Vector Knowledge Base")
print("-" * 70)
try:
    vector_kb = VectorKnowledgeBase()
    if vector_kb.service:
        test_query = "C'est quoi l'ENSA ?"
        results = vector_kb.search(test_query, top_k=3, threshold=0.5)
        
        if results:
            print(f"✅ Found {len(results)} results for: '{test_query}'")
            for i, result in enumerate(results, 1):
                print(f"   [{i}] Score: {result['score']:.2f} | Category: {result['metadata'].get('category', 'N/A')}")
                print(f"       Text: {result['text'][:80]}...")
        else:
            print("⚠️ No results found in vector search")
    else:
        print("❌ Vector knowledge base not initialized")
except Exception as e:
    print(f"❌ Error: {e}")

# ===== Test 3: Prompt Building =====
print("\n[TEST 3] Prompt Building with Context")
print("-" * 70)
try:
    # Mock search results
    mock_results = [
        {
            'text': "L'ENSA (École Nationale des Sciences Appliquées) est une école d'ingénieurs publique marocaine.",
            'metadata': {'category': 'Écoles', 'question': "C'est quoi l'ENSA ?"},
            'score': 0.92
        },
        {
            'text': "Pour s'inscrire à l'ENSA, il faut avoir un bac scientifique et passer le concours CNC.",
            'metadata': {'category': 'Admissions', 'question': 'Admission ENSA'},
            'score': 0.85
        }
    ]
    
    prompt = YAFIPromptEngine.build_prompt(
        query="Comment accéder à l'ENSA ?",
        search_results=mock_results,
        history=[]
    )
    
    print("✅ Prompt Generated Successfully")
    print(f"   Length: {len(prompt)} characters")
    print(f"   Preview: {prompt[:200]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# ===== Test 4: LLM with Context (RAG) =====
print("\n[TEST 4] LLM Response with RAG Context")
print("-" * 70)
try:
    mock_results = [
        {
            'text': "L'ENSA est une école d'ingénieurs publique créée pour former des ingénieurs de haut niveau.",
            'metadata': {'category': 'Écoles', 'question': "C'est quoi l'ENSA ?"},
            'score': 0.90
        }
    ]
    
    prompt = YAFIPromptEngine.build_prompt(
        query="Parle-moi de l'ENSA",
        search_results=mock_results,
        history=[]
    )
    
    llm_response = llm_engine.ask(prompt)
    
    if llm_response:
        formatted_response = YAFIPromptEngine.format_response(
            llm_response,
            search_results=mock_results,
            add_citations=True
        )
        print("✅ LLM Generated Response with Citations:")
        print(f"\n{formatted_response[:300]}...")
    else:
        print("❌ No response from LLM")
except Exception as e:
    print(f"❌ Error: {e}")

# ===== Test 5: Full End-to-End Test =====
print("\n[TEST 5] End-to-End Scenario")
print("-" * 70)
try:
    # Initialize session
    session_id = "test_session_001"
    conversation_manager.add_message(session_id, 'user', "C'est quoi ENCG ?")
    
    # Search
    vector_kb = VectorKnowledgeBase()
    search_results = vector_kb.search("ENCG école commerce", top_k=2, threshold=0.5) if vector_kb.service else None
    
    if search_results:
        # Build prompt
        history = conversation_manager.get_history(session_id, last_n=2)
        prompt = YAFIPromptEngine.build_prompt(
            query="C'est quoi ENCG ?",
            search_results=search_results,
            history=history
        )
        
        # Generate response
        llm_response = llm_engine.ask(prompt)
        
        if llm_response:
            formatted = YAFIPromptEngine.format_response(
                llm_response,
                search_results=search_results,
                add_citations=True
            )
            
            # Save to history
            conversation_manager.add_message(session_id, 'assistant', formatted)
            
            print(f"✅ Full E2E Test Successful")
            print(f"   Session ID: {session_id}")
            print(f"   Found {len(search_results)} search results")
            print(f"   Generated response: {len(formatted)} chars")
            print(f"\n   Preview:\n   {formatted[:250]}...")
        else:
            print("❌ LLM generation failed")
    else:
        print("⚠️ No search results found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# ===== Summary =====
print("\n" + "=" * 70)
print("✅ OLLAMA INTEGRATION TEST COMPLETE")
print("=" * 70)
print("\n🎯 Next Steps:")
print("   1. Verify Ollama is accessible at http://localhost:11434")
print("   2. Ensure llama3.2:1b model is downloaded")
print("   3. Check vector knowledge base is built (run build_vector_index.py)")
print("   4. Start server with: python backend/server.py")
print("   5. Test via API: http://localhost:5000/chat")
print("\n")
