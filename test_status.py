#!/usr/bin/env python3
"""Simple test runner - identify and fix problems"""

import os
import sys

print("\n" + "="*70)
print("YAFI - QUICK TEST & FIX")
print("="*70 + "\n")

# Step 1: Check if servers are running
print("STEP 1: Check Servers...")
import subprocess
import socket
import time

def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

ports = {
    5000: "OLD Server",
    5001: "NEW Server",
    11435: "Ollama"
}

for port, name in ports.items():
    if is_port_open(port):
        print(f"  {name} (:{port}): RUNNING OK")
    else:
        print(f"  {name} (:{port}): NOT RUNNING - Need to start")

# Step 2: Simple import test
print("\nSTEP 2: Check Imports...")
try:
    import requests
    print("  requests: OK")
except:
    print("  requests: MISSING - Run: pip install requests")
    sys.exit(1)

try:
    import json
    print("  json: OK")
except:
    print("  json: MISSING")
    sys.exit(1)

# Step 3: Test connectivity
print("\nSTEP 3: Test Connectivity...")
try:
    r = requests.get("http://localhost:5000/", timeout=2)
    print("  OLD Server: REACHABLE")
except:
    print("  OLD Server: NOT REACHABLE - Start: python backend/server.py")

try:
    r = requests.get("http://localhost:5001/", timeout=2)
    print("  NEW Server: REACHABLE")
except:
    print("  NEW Server: NOT REACHABLE - Start: python backend/server_optimized.py")

try:
    r = requests.get("http://localhost:11435/api/tags", timeout=2)
    print("  Ollama: REACHABLE")
except:
    print("  Ollama: NOT REACHABLE - Start Ollama application")

# Step 4: Run simple test
print("\nSTEP 4: Test Simple Question...")
test_question = "Bonjour"

try:
    r = requests.post(
        "http://localhost:5001/chat",
        json={"message": test_question, "session_id": "test"},
        timeout=5
    )
    if r.status_code == 200:
        response = r.json()
        resp_text = response.get("response", "")
        print(f"  NEW Server response: {len(resp_text)} chars")
        if len(resp_text) > 10:
            print(f"  Sample: {resp_text[:100]}...")
            print("  Status: OK")
        else:
            print("  Status: EMPTY - Ollama might not be working")
    else:
        print(f"  HTTP Error: {r.status_code}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70 + "\n")

if not is_port_open(5000):
    print("1. Start ON Server (Terminal 1):")
    print("   cd backend")
    print("   python server.py\n")

if not is_port_open(5001):
    print("2. Start NEW Server (Terminal 2):")
    print("   cd backend")  
    print("   python server_optimized.py\n")

if not is_port_open(11435):
    print("3. Start Ollama (Terminal 3 or Ollama app):")
    print("   ollama serve\n")

print("4. Then run tests:")
print("   python test_complex_questions.py\n")

print("="*70)
