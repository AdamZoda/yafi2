import requests
import json
import sys
import os

# Emulate environment for test
os.environ["USE_LLM"] = "true"
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["LLM_MODEL"] = "llama3.2:1b"

try:
    from llm_engine import llm_engine
    print("✅ LLM Engine loaded")
except ImportError:
    print("❌ Could not import llm_engine")
    sys.exit(1)

def test_ollama_connection():
    print("Testing connection to Ollama (http://localhost:11434)...")
    try:
        response = requests.get("http://localhost:11434/")
        if response.status_code == 200:
            print("✅ Ollama is running!")
        else:
            print(f"⚠️ Ollama returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Ollama is NOT running or not reachable: {e}")
        print("💡 Make sure to run 'ollama serve' and have the model downloaded.")

def test_generation():
    print("\nTesting LLM Generation...")
    test_prompt = "Dis bonjour en tant qu'assistant YAFI."
    response = llm_engine.ask(test_prompt)
    
    if response:
        print(f"✅ LLM Response: {response}")
    else:
        print("❌ LLM failed to generate a response.")

if __name__ == "__main__":
    test_ollama_connection()
    test_generation()
