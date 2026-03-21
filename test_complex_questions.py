#!/usr/bin/env python3
"""
Test Complex Questions - Advanced Testing Framework
Test 22 complex questions to verify Ollama is working well
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List

# Configuration
SERVERS = {
    "old": "http://localhost:5000",
    "new": "http://localhost:5001",
}

COMPLEX_QUESTIONS = [
    {
        "id": "Q1",
        "category": "Dilemme Personnel",
        "question": "J'aime beaucoup les maths et la bio, mais j'adore aussi le dessin. Je ne sais pas si je dois faire ingénierie ou architecture. Comment choisir? Ma moyenne est 14.",
        "expected_length": 300,
    },
    {
        "id": "Q2",
        "category": "Question Paradoxale",
        "question": "Est-ce que c'est possible de faire médecine si je suis PC et non SVT? Et si j'ai 12 de moyenne?",
        "expected_length": 250,
    },
    {
        "id": "Q3",
        "category": "Situation Complexe",
        "question": "Je viens d'une petite famille pauvre, je dois réussir pour aider mes parents. Quel domaine offre les meilleurs débouchés rapidement?",
        "expected_length": 350,
    },
    {
        "id": "Q4",
        "category": "Comparaison de Filières",
        "question": "Quelle différence entre ENSA, EMSI et UIR? Je veux étudier l'informatique avec 13 de moyenne et budget limité.",
        "expected_length": 300,
    },
    {
        "id": "Q5",
        "category": "Stratégie Multi-Étapes",
        "question": "Mon plan c'est: 1) Faire FST maintenant, 2) Master après, 3) Partir à l'étranger. Est-ce viable? Quels pays acceptent?",
        "expected_length": 300,
    },
    {
        "id": "Q6",
        "category": "Contingent de Vie",
        "question": "Ma copine veut rester au Maroc, moi je veux partir. On veut pas se quitter. Comment gérer ça avec les études?",
        "expected_length": 280,
    },
    {
        "id": "Q7",
        "category": "Question Timing",
        "question": "Je suis en première, il me reste 1 an. Mes moyennes sont: Maths 16, Français 8, Philo 7. Qu'est-ce que je dois faire maintenant pour réussir?",
        "expected_length": 300,
    },
    {
        "id": "Q8",
        "category": "Piège du Prestige",
        "question": "Tous les gens prestigieux viennent de Médecine. Est-ce que je dois y aller même si j'aime l'informatique?",
        "expected_length": 250,
    },
    {
        "id": "Q9",
        "category": "Question Double-Sens",
        "question": "Je veux un métier cool et qu'on me respecte. C'est possible avec commerce/management?",
        "expected_length": 200,
    },
    {
        "id": "Q10",
        "category": "Cas Spécial",
        "question": "J'ai un handicap moteur. Quelles études me sont accessibles? Je veux contribuer à la société quand même.",
        "expected_length": 300,
    },
    {
        "id": "Q11",
        "category": "Étudiant Très Brillant",
        "question": "J'ai 19 de moyenne, bac SM, je pourrais faire n'importe quoi. Par quoi je commence?",
        "expected_length": 280,
    },
    {
        "id": "Q12",
        "category": "Étudiant en Difficulté",
        "question": "Ma moyenne est 9. Les gens disent que j'ai échoué. Mais je suis motivé. Qu'est-ce que je fais?",
        "expected_length": 300,
    },
    {
        "id": "Q13",
        "category": "Philosophique",
        "question": "Et si je me trompe dans mon choix? Comment je pourrais changer après?",
        "expected_length": 250,
    },
    {
        "id": "Q14",
        "category": "Existentiel",
        "question": "Qu'est-ce qui compte vraiment dans le choix de filière: l'argent, la passion, ou le statut social?",
        "expected_length": 300,
    },
    {
        "id": "Q15",
        "category": "Deux Domaines Opposés",
        "question": "Je veux faire médecine ET informatique. Ça existe? Comment combiner?",
        "expected_length": 250,
    },
    {
        "id": "Q16",
        "category": "Cas Limite Temporel",
        "question": "Je viens juste de savoir que le bac c'est dans 2 mois et j'ai pas réviser. Par quoi je commence pour pas perdre l'année?",
        "expected_length": 300,
    },
    {
        "id": "Q17",
        "category": "Pression Familiale",
        "question": "Ma mère veut que je sois docteur (médecin). Moi je veux informatique. Comment discuter sans conflict?",
        "expected_length": 300,
    },
    {
        "id": "Q18",
        "category": "Peer Pressure",
        "question": "Tous mes copains font ENSA. Moi je veux faire chose différente. C'est bête de pas suivre?",
        "expected_length": 250,
    },
    {
        "id": "Q19",
        "category": "Technique + Psycho",
        "question": "Je veux étudier psychologie mais j'adore aussi la technologie. Genre psychologie computationnelle?",
        "expected_length": 250,
    },
    {
        "id": "Q20",
        "category": "Question Économique + Personnelle",
        "question": "Mon père est malade, je dois travailler pendant les études. Quelle filière me laisse du temps?",
        "expected_length": 300,
    },
    {
        "id": "Q21",
        "category": "Connaissances Mal Structurées",
        "question": "J'aime les gens, j'aime parler, j'aime organiser des événements. Je suis pas fort en maths. Qu'est-ce que je fais?",
        "expected_length": 250,
    },
    {
        "id": "Q22",
        "category": "Confusion Totale",
        "question": "Je sais pas. Je comprends pas. Tout est confus. Aider moi.",
        "expected_length": 200,
    },
]

def test_server(server_name: str, server_url: str, question: str, session_id: str) -> Dict:
    """Test a single question on a server"""
    try:
        response = requests.post(
            f"{server_url}/chat",
            json={"message": question, "session_id": session_id},
            timeout=15
        )
        data = response.json()
        
        return {
            "status": "OK",
            "response": data.get("response", ""),
            "length": len(data.get("response", "")),
            "source": data.get("source", "unknown"),
            "time": response.elapsed.total_seconds(),
        }
    except requests.exceptions.ConnectError:
        return {"status": "ERROR", "error": "Server not running", "time": 0}
    except requests.exceptions.Timeout:
        return {"status": "TIMEOUT", "error": "Request timeout (15s)", "time": 15}
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "time": 0}

def score_response(response: Dict, expected_length: int) -> int:
    """Score response quality 1-10"""
    if response.get("status") != "OK":
        return 0
    
    length = response.get("length", 0)
    
    # Scoring logic
    if length < 50:
        return 1  # Too short
    elif length < expected_length * 0.5:
        return 3  # Short
    elif length < expected_length * 0.8:
        return 5  # Okay
    elif length < expected_length * 1.2:
        return 7  # Good
    elif length < expected_length * 2:
        return 9  # Very good
    else:
        return 8  # Long but maybe too long
    
    return 5

def main():
    print("=" * 70)
    print("COMPLEX QUESTIONS TEST - Advanced Framework")
    print("22 Sophisticated Questions")
    print("=" * 70 + "\n")
    
    # Check servers
    print("Checking servers...")
    servers_available = {}
    
    for name, url in SERVERS.items():
        try:
            requests.get(url, timeout=2)
            print(f"✓ {name.upper()} server running on {url}")
            servers_available[name] = True
        except:
            print(f"✗ {name.upper()} server NOT running on {url}")
            servers_available[name] = False
    
    if not any(servers_available.values()):
        print("\n❌ No servers running!")
        return
    
    print(f"\n{'='*70}")
    print(f"Testing {len(COMPLEX_QUESTIONS)} complex questions...")
    print(f"{'='*70}\n")
    
    results = []
    
    for idx, q_data in enumerate(COMPLEX_QUESTIONS, 1):
        question_id = q_data["id"]
        category = q_data["category"]
        question = q_data["question"]
        expected_length = q_data["expected_length"]
        
        print(f"[{idx:2d}/{len(COMPLEX_QUESTIONS)}] {question_id}: {category}")
        print(f"     Q: {question[:60]}...")
        
        test_results = {}
        
        for server_name in SERVERS:
            if servers_available[server_name]:
                result = test_server(
                    server_name,
                    SERVERS[server_name],
                    question,
                    f"complex_test_{idx}"
                )
                test_results[server_name] = result
                
                if result.get("status") == "OK":
                    score = score_response(result, expected_length)
                    print(f"     {server_name.upper()}: {result['length']} chars | Score: {score}/10 | {result['time']:.1f}s")
                else:
                    print(f"     {server_name.upper()}: {result.get('error', 'Unknown error')}")
        
        results.append({
            "id": question_id,
            "category": category,
            "question": question,
            "results": test_results,
        })
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY ANALYSIS")
    print("="*70)
    
    if servers_available.get("new"):
        scores = []
        for r in results:
            if "new" in r["results"]:
                result = r["results"]["new"]
                score = score_response(result, r.get("expected_length", 250))
                scores.append(score)
        
        if scores:
            avg_score = sum(scores) / len(scores)
            excellent = len([s for s in scores if s >= 9])
            good = len([s for s in scores if 7 <= s < 9])
            okay = len([s for s in scores if 5 <= s < 7])
            poor = len([s for s in scores if s < 5])
            
            print(f"\nNEW Server Performance:")
            print(f"  Average Score: {avg_score:.1f}/10")
            print(f"  Excellent (9-10): {excellent}/22 ⭐")
            print(f"  Good (7-8): {good}/22 ✓")
            print(f"  Okay (5-6): {okay}/22 ~")
            print(f"  Poor (<5): {poor}/22 ✗")
            
            if avg_score >= 7:
                print(f"\n✅ NEW Server PASSES complex question test!")
            elif avg_score >= 5:
                print(f"\n⚠️ NEW Server is OKAY but could be better")
            else:
                print(f"\n❌ NEW Server struggles with complex questions")
    
    # Save results
    filename = f"complex_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Results saved to {filename}")
    
    # Sample responses
    print("\n" + "="*70)
    print("SAMPLE RESPONSES (First 3 questions)")
    print("="*70)
    
    for i in range(min(3, len(results))):
        r = results[i]
        print(f"\n{r['id']}: {r['category']}")
        print(f"Q: {r['question'][:80]}...")
        
        if "new" in r["results"] and r["results"]["new"].get("status") == "OK":
            response = r["results"]["new"]["response"]
            print(f"NEW Response ({len(response)} chars):")
            print(f"  {response[:200]}...")

if __name__ == "__main__":
    main()
