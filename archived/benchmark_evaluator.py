import requests
import json
import time
import sys

API_URL = "http://localhost:5000/chat"

def safe_print(text):
    try:
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    except:
        print(text.encode('ascii', errors='replace').decode('ascii'))

def run_benchmark():
    try:
        with open('backend/benchmark_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            questions = data['benchmark_questions']
    except Exception as e:
        safe_print(f"Error loading questions: {e}")
        return

    safe_print("\n" + "="*80)
    safe_print("YAFI BENCHMARK: IA vs PROLOG EXPERT")
    safe_print("="*80 + "\n")

    results = []
    
    for item in questions:
        q_id = item['id']
        question = item['question']
        truth = item['expert_truth']
        
        safe_print(f"TEST #{q_id}: {question}")
        safe_print(f"Truth: {truth}")
        
        start_time = time.time()
        try:
            # Note: We use stream=False for easier benchmarking, 
            # but server_optimized handles both.
            response = requests.post(API_URL, json={
                "message": question,
                "userId": "benchmark_user",
                "stream": False
            }, timeout=80)
            
            elapsed = round((time.time() - start_time), 2)
            
            if response.status_code == 200:
                ai_resp = response.json().get('response', 'NO_RESPONSE')
                safe_print(f"AI ({elapsed}s): {ai_resp[:150]}...")
                
                # Basic overlap check (Simple metric)
                truth_words = set(truth.lower().split())
                ai_words = set(ai_resp.lower().split())
                overlap = len(truth_words.intersection(ai_words))
                score = round((overlap / len(truth_words)) * 100) if truth_words else 0
                
                safe_print(f"Accuracy Score: {score}%")
                results.append({"id": q_id, "score": score, "time": elapsed})
            else:
                safe_print(f"Server Error: {response.status_code}")
                results.append({"id": q_id, "score": 0, "error": response.status_code})
                
        except Exception as e:
            safe_print(f"Connection Error: {e}")
            results.append({"id": q_id, "score": 0, "error": str(e)})
            
        safe_print("-" * 40)
        time.sleep(1)

    safe_print("\n" + "="*80)
    safe_print("BENCHMARK SUMMARY")
    total_score = sum(r.get('score', 0) for r in results)
    total_time = sum(r.get('time', 0) for r in results)
    avg_score = total_score / len(results) if results else 0
    avg_time = total_time / len(results) if results else 0
    safe_print(f"Average Accuracy: {round(avg_score, 1)}%")
    safe_print(f"Average Time: {round(avg_time, 2)}s")
    safe_print("="*80 + "\n")

if __name__ == "__main__":
    run_benchmark()
