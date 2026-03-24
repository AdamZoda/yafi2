import requests
import time

FAST_SUGGESTIONS = [
    "Différence entre Licence Pro et Fondamentale",
    "Puis-je faire médecine avec 14 de moyenne ?",
    "Comment devenir ingénieur en cybersécurité ?"
]

def evaluate_fast():
    print("="*60)
    print("🚀 FAST EVALUATION")
    print("="*60)
    
    for i, q in enumerate(FAST_SUGGESTIONS, 1):
        print(f"\n[{i}/3] QUESTION : {q}")
        try:
            res = requests.post("http://localhost:5000/chat", json={
                "message": q,
                "session_id": "eval_fast",
                "stream": False
            }, timeout=90)
            data = res.json()
            source = data.get("source", "UNKNOWN")
            text = data.get("response", "")
            
            print(f"  SOURCE : {source}")
            print(f"  REPONSE: {text[:150].replace(chr(10), ' ')}...")
            
        except Exception as e:
            print(f"  ❌ ERREUR : {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    evaluate_fast()
