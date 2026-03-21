import requests

with open("test_out.txt", "w", encoding="utf-8") as f:
    f.write("TEST 1: Set Intent (Prix EMSI)\n")
    r1 = requests.post('http://127.0.0.1:5000/chat', json={'message':'Prix de EMSI', 'session_id':'mem_test'})
    f.write(r1.json()['response'] + "\n\n")

    f.write("TEST 2: Context Retrieval (Et pour UIR ?)\n")
    r2 = requests.post('http://127.0.0.1:5000/chat', json={'message':'Et pour UIR ?', 'session_id':'mem_test'})
    f.write(r2.json()['response'] + "\n\n")

    f.write("TEST 3: Dynamic Routing (Durée ENSA)\n")
    r3 = requests.post('http://127.0.0.1:5000/chat', json={'message':'Quelle est la duree des etudes a ENSA ?', 'session_id':'mem_test2'})
    f.write(r3.json()['response'] + "\n")

