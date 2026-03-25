import requests
import json
import time
import sys

# Force UTF-8 for Windows Console
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = "http://127.0.0.1:5000/chat"
QUESTIONS = [
    "Quelles sont les filieres de l'ENSA Marrakech ?",
    "J'ai 15 de moyenne en Bac SM, quel conseil pour l'orientation ?",
    "Ecoles de commerce a Casablanca avec un budget de moins de 45000 DH/an",
    "Quelle est la difference entre l'ENCG et l'ENSA ?",
    "Je suis tres stresse pour les concours de medecine, aide-moi."
]

def run_bench():
    print("="*60)
    print("YAFI PERFORMANCE TEST - QWEN 2.5:3B (16GB RAM)")
    print("="*60)
    
    total_time = 0
    results = []

    for i, q in enumerate(QUESTIONS):
        print(f"\n[Test {i+1}/5] Question: {q}")
        start = time.time()
        
        try:
            resp = requests.post(URL, json={"message": q, "session_id": f"bench_{i}"})
            elapsed = time.time() - start
            data = resp.json()
            
            # Use ASCII indicators instead of Emojis for terminal safety
            print(f"-- Time: {elapsed:.2f}s")
            
            response_text = data.get('response', '')
            print(f"-- YAFI: {response_text[:150]}...")
            
            results.append({
                "question": q,
                "time": elapsed,
                "response": response_text
            })
            total_time += elapsed
        except Exception as e:
            print(f"-- Error: {str(e)}")

    print("\n" + "="*60)
    print(f"SUMMARY: Average {total_time/5:.2f}s per response.")
    print("="*60)

if __name__ == "__main__":
    run_bench()
