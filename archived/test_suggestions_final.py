import requests
import json

BASE_URL = "http://127.0.0.1:5000/chat"

TEST_QUERIES = [
    "Comparer EMSI et UIR",
    "Frais de scolarité de l'ISCAE",
    "Est-ce que l'UIR a un internat ?",
    "Comment s'inscrire sur CursusSup ?",
    "Parle moi de l'ENAM",
    "Menu de la cantine à l'UIK"
]

def run_tests():
    print("="*60)
    print("FINAL SUGGESTION VERIFICATION")
    print("="*60)
    
    for i, q in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{len(TEST_QUERIES)}] QUESTION : {q}")
        try:
            resp = requests.post(BASE_URL, json={"message": q, "session_id": "test_suggestions"})
            data = resp.json()
            print(f"  SOURCE : {data.get('source')}")
            resp_text = data.get('response', '')
            try:
                print(f"  REPONSE: {resp_text[:300]}...")
            except UnicodeEncodeError:
                print(f"  REPONSE: {resp_text[:300].encode('ascii', 'ignore').decode('ascii')}... (emojis stripped)")
        except Exception as e:
            print(f"  ERROR : {e}")

if __name__ == "__main__":
    run_tests()
