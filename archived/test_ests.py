import requests
import time

EST_TESTS = [
    "Où se trouve l'EST ?",
    "Quelles sont les filières de l'ESTS ?",
    "Quelles sont les filières de l'EST Safi ?",
    "Puis-je faire l'ESTS avec 14.5 ?",
    "EST à Casablanca",
    "Filière GI à l'ESTS",
    "Score seuil pour l'ESTS"
]

def test_ests():
    print("="*60)
    print("EST / ESTS VERIFICATION")
    print("="*60)
    
    for i, q in enumerate(EST_TESTS, 1):
        print(f"\n[{i}/{len(EST_TESTS)}] QUESTION : {q}")
        try:
            res = requests.post("http://localhost:5000/chat", json={
                "message": q,
                "session_id": "test_ests",
                "stream": False
            }, timeout=30)
            data = res.json()
            source = data.get("source", "UNKNOWN")
            text = data.get("response", "")
            
            # Print with error handling for Windows console
            output = f"  SOURCE : {source}\n  REPONSE: {text[:200]}..."
            print(output.encode('ascii', 'ignore').decode('ascii'))
            
        except Exception as e:
            print(f"  ERROR : {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    test_ests()
