#!/usr/bin/env python3
"""
YAFI Ollama Integration - Demo & Usage Examples
Shows how to interact with the new RAG + Ollama system
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:5000"  # Main server
TEST_SERVER_URL = "http://localhost:5001"  # Test server

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(response_data, title="Response"):
    print(f"\n📝 {title}:")
    print(f"{response_data}\n")

# ============================================================
# Example 1: Test Ollama Direct Connection
# ============================================================
def example_1_test_ollama():
    print_section("Example 1: Test Ollama Direct Connection")
    
    print("🧪 Testing direct Ollama connection...")
    
    payload = {
        "prompt": "Tu es YAFI, un assistant d'orientation marocain. Explique en 2 phrases ce qu'est une école d'ingénieurs."
    }
    
    response = requests.post(
        f"{TEST_SERVER_URL}/api/test/ollama",
        json=payload,
        timeout=120
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"   Model: {data.get('model')}")
        print(f"   Provider: {data.get('provider')}")
        print_response(data.get('response'), "Ollama Response")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

# ============================================================
# Example 2: Test RAG + Ollama (Full Pipeline)
# ============================================================
def example_2_test_rag_full():
    print_section("Example 2: Full RAG + Ollama Pipeline")
    
    questions = [
        "C'est quoi l'ENSA ?",
        "Quelle école pour informatique ?",
        "Comment s'inscrire à ENCG ?"
    ]
    
    for question in questions:
        print(f"❓ Question: {question}")
        
        payload = {
            "query": question,
            "session_id": "demo_session"
        }
        
        try:
            response = requests.post(
                f"{TEST_SERVER_URL}/api/test/full",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Method: {data.get('method')}")
                print(f"   📊 Confidence: {data.get('confidence', 0):.0%}")
                print(f"   📚 Sources: {', '.join(data.get('sources', []))}")
                print(f"   💬 Response Preview: {data.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print()

# ============================================================
# Example 3: Test System Health
# ============================================================
def example_3_system_health():
    print_section("Example 3: Check System Health & Status")
    
    print("🏥 Checking system components...\n")
    
    # Check health
    response = requests.get(f"{TEST_SERVER_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        components = data.get('components', {})
        
        print("✅ Vector KB Available:", components.get('vector_kb_available'))
        print("✅ LLM Available:", components.get('llm_available'))
        
        llm_health = components.get('llm_health', {})
        print(f"\n   LLM Details:")
        print(f"   - Provider: {llm_health.get('provider')}")
        print(f"   - Model: {llm_health.get('model')}")
        print(f"   - Enabled: {llm_health.get('enabled')}")
        print(f"   - Available: {llm_health.get('available')}")
    else:
        print(f"❌ Health check failed: {response.status_code}")

# ============================================================
# Example 4: Available Models
# ============================================================
def example_4_available_models():
    print_section("Example 4: List Available Ollama Models")
    
    response = requests.get(f"{TEST_SERVER_URL}/api/info/models", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        
        print(f"Found {data.get('count')} models:\n")
        
        for model in models:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0)
            size_gb = size / (1024**3)
            print(f"  📦 {name}")
            print(f"     Size: {size_gb:.2f} GB")
            print()
    else:
        print(f"❌ Error: {response.status_code}")

# ============================================================
# Example 5: Simulate Real Student Conversation
# ============================================================
def example_5_student_conversation():
    print_section("Example 5: Simulate Student Conversation")
    
    session_id = "student_123"
    questions = [
        ("Bonjour, j'ai un Bac PC avec 14 de moyenne", "student_greeting"),
        ("Quelle école pour l'informatique ?", "school_query"),
        ("Et pour l'architecture ?", "followup_query"),
        ("Combien ça coûte ?", "cost_query"),
    ]
    
    for question, context in questions:
        print(f"\n👨‍🎓 Student: \"{question}\" ({context})")
        
        payload = {
            "query": question,
            "session_id": session_id
        }
        
        try:
            response = requests.post(
                f"{TEST_SERVER_URL}/api/test/full",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('response', 'No response')
                method = data.get('method', 'unknown')
                confidence = data.get('confidence', 0)
                
                # Print abbreviated response
                preview = bot_response[:200] + "..." if len(bot_response) > 200 else bot_response
                print(f"🤖 YAFI ({method}, {confidence:.0%}): {preview}")
            else:
                print(f"🤖 YAFI: Error - {response.status_code}")
                
        except Exception as e:
            print(f"🤖 YAFI: Connection error - {e}")
        
        # Small delay between requests
        time.sleep(1)

# ============================================================
# Example 6: Performance Benchmark
# ============================================================
def example_6_performance_benchmark():
    print_section("Example 6: Performance Benchmark")
    
    queries = [
        "C'est quoi ENSA ?",
        "Écoles pour médecine",
        "Seuil admission ENCG"
    ]
    
    print("Measuring response times...\n")
    
    times = []
    for query in queries:
        start = time.time()
        
        try:
            response = requests.post(
                f"{TEST_SERVER_URL}/api/test/full",
                json={"query": query, "session_id": "benchmark"},
                timeout=120
            )
            
            elapsed = time.time() - start
            times.append(elapsed)
            
            status = "✅" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"{status} '{query[:30]}...' - {elapsed:.1f}s")
        except Exception as e:
            print(f"❌ '{query}'  - Error: {e}")
    
    if times:
        print(f"\n📊 Benchmark Results:")
        print(f"   Average: {sum(times)/len(times):.1f}s")
        print(f"   Min: {min(times):.1f}s")
        print(f"   Max: {max(times):.1f}s")

# ============================================================
# Main Menu
# ============================================================
def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║     YAFI Ollama Integration - Demo & Usage Examples        ║
║                                                            ║
║  This script demonstrates the new RAG + Ollama system      ║
║  for intelligent student orientation responses.           ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📡 Verifying server connections...\n")
    
    # Check if servers are running
    try:
        requests.get(f"{TEST_SERVER_URL}/health", timeout=2)
        print("✅ Test server is running (port 5001)")
    except:
        print("❌ Test server NOT running on port 5001")
        print("   Run: python test_server.py")
        return
    
    print("\nAvailable Examples:")
    print("  1. Test Ollama Direct Connection")
    print("  2. Test Full RAG + Ollama Pipeline")
    print("  3. Check System Health & Status")
    print("  4. List Available Models")
    print("  5. Simulate Student Conversation")
    print("  6. Performance Benchmark")
    print("  9. Run All Examples")
    print("  0. Exit")
    
    while True:
        choice = input("\nSelect example to run (0-9): ").strip()
        
        if choice == "1":
            example_1_test_ollama()
        elif choice == "2":
            example_2_test_rag_full()
        elif choice == "3":
            example_3_system_health()
        elif choice == "4":
            example_4_available_models()
        elif choice == "5":
            example_5_student_conversation()
        elif choice == "6":
            example_6_performance_benchmark()
        elif choice == "9":
            print("\n⏳ Running all examples...")
            example_3_system_health()
            example_4_available_models()
            example_1_test_ollama()
            example_2_test_rag_full()
            example_5_student_conversation()
            example_6_performance_benchmark()
            break
        elif choice == "0":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted!\n")
    except Exception as e:
        print(f"\n\n❌ Error: {e}\n")
