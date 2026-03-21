#!/usr/bin/env python3
"""
🧪 YAFI - Automated Test Script
Teste auto les questions et génère un rapport
"""

import requests
import json
import time
from datetime import datetime

class YAFITestRunner:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.results = []
        self.session_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def test_question(self, question: str, category: str, expected_mode: str = "NORMAL"):
        """Tester une question et noter les résultats"""
        
        print(f"\n{'─'*70}")
        print(f"❓ {category}: {question}")
        print(f"   Mode attendu: {expected_mode}")
        
        try:
            response = requests.post(
                f"{self.backend_url}/chat",
                json={
                    "message": question,
                    "session_id": self.session_id
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '')
                
                # Calculer les metrics
                length = len(answer)
                has_emojis = any(ord(c) > 127 for c in answer)
                is_question_at_end = answer.strip().endswith('?')
                
                # Déterminer la qualité
                if length < 100:
                    quality = "❌ COURT"
                elif length < 300:
                    quality = "⚠️  MOYEN"
                elif length < 500:
                    quality = "✅ BON"
                else:
                    quality = "✨ EXCELLENT"
                
                print(f"   Status: {quality}")
                print(f"   Longueur: {length} caractères")
                print(f"   Emojis: {'✅' if has_emojis else '❌'}")
                print(f"   Q finale: {'✅' if is_question_at_end else '❌'}")
                
                # Afficher un extrait
                excerpt = answer[:150] + "..." if len(answer) > 150 else answer
                print(f"   Réponse: {excerpt}")
                
                # Sauvegarder le résultat
                self.results.append({
                    'question': question,
                    'category': category,
                    'mode': expected_mode,
                    'length': length,
                    'quality': quality,
                    'has_emojis': has_emojis,
                    'full_response': answer[:500]  # Sauvegarder 500 premiers chars
                })
                
                return True
                
            else:
                print(f"   ❌ HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
            return False
    
    def run_full_test(self):
        """Exécuter la suite de tests complète"""
        
        print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🧪 YAFI - TEST AUTOMATIQUE OLLAMA PERMISSIONS                   ║
║                                                                            ║
║                 Cette suite teste 30 questions d'orientation              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Vérifier le backend
        print("🔍 Vérification du backend...")
        try:
            resp = requests.get(f"{self.backend_url}/health", timeout=5)
            if resp.status_code == 200:
                print("✅ Backend accessible\n")
            else:
                print(f"❌ Backend répond mal ({resp.status_code})")
                return
        except:
            print("❌ Backend non accessible (lancez: python server.py)")
            return
        
        # Tests CRÉATIF
        print(f"\n{'='*70}")
        print("PHASE 1: Questions Courtes (Mode CRÉATIF)")
        print(f"{'='*70}")
        
        creative_questions = [
            ("c'est quoi cv?", "Courte 1"),
            ("bonjour", "Courte 2"),
            ("aide", "Courte 3"),
            ("pourquoi?", "Courte 4"),
            ("comment?", "Courte 5"),
        ]
        
        for q, cat in creative_questions:
            self.test_question(q, cat, "CRÉATIF")
            time.sleep(1)
        
        # Tests PREMIUM
        print(f"\n{'='*70}")
        print("PHASE 2: Questions Conseil (Mode PREMIUM)")
        print(f"{'='*70}")
        
        premium_questions = [
            ("Comment je dois choisir mon orientation?", "Conseil 1"),
            ("Donne-moi un conseil pour bien choisir ma filière", "Conseil 2"),
            ("Comment je peux être sûr(e) de mon choix?", "Conseil 3"),
            ("Quel est le meilleur domaine pour étudier?", "Conseil 4"),
            ("Donne-moi une motivation pour étudier!", "Conseil 5"),
        ]
        
        for q, cat in premium_questions:
            self.test_question(q, cat, "PREMIUM")
            time.sleep(1)
        
        # Tests NORMAL
        print(f"\n{'='*70}")
        print("PHASE 3: Questions Spécifiques (Mode NORMAL)")
        print(f"{'='*70}")
        
        normal_questions = [
            ("Quelles sont les meilleures écoles d'informatique?", "Spécifique 1"),
            ("Quelle est la différence entre ENSA et EMSI?", "Spécifique 2"),
            ("Comment s'inscrire à Minhaty?", "Spécifique 3"),
            ("Que faire après le Bac?", "Spécifique 4"),
            ("Quels sont les débouchés de l'informatique?", "Spécifique 5"),
        ]
        
        for q, cat in normal_questions:
            self.test_question(q, cat, "NORMAL")
            time.sleep(1)
        
        # Générer le rapport
        self.generate_report()
    
    def generate_report(self):
        """Générer un rapport des tests"""
        
        print(f"\n\n{'='*70}")
        print("📊 RAPPORT DE TEST FINAL")
        print(f"{'='*70}\n")
        
        # Statistiques
        total = len(self.results)
        excellent = sum(1 for r in self.results if "EXCELLENT" in r['quality'])
        bon = sum(1 for r in self.results if "BON" in r['quality'])
        moyen = sum(1 for r in self.results if "MOYEN" in r['quality'])
        court = sum(1 for r in self.results if "COURT" in r['quality'])
        
        avg_length = sum(r['length'] for r in self.results) / total if total > 0 else 0
        
        print(f"Total testé: {total} questions\n")
        print(f"Résultats:")
        print(f"  ✨ EXCELLENT:  {excellent} ({excellent/total*100:.0f}%)")
        print(f"  ✅ BON:        {bon} ({bon/total*100:.0f}%)")
        print(f"  ⚠️  MOYEN:     {moyen} ({moyen/total*100:.0f}%)")
        print(f"  ❌ COURT:      {court} ({court/total*100:.0f}%)")
        print(f"\nLongueur moyenne: {avg_length:.0f} caractères")
        
        # Verdict
        print(f"\n{'─'*70}")
        print("🎯 VERDICT")
        print(f"{'─'*70}\n")
        
        if excellent >= total * 0.6:
            print("✨ SUCCÈS! Ollama Advanced Permissions fonctionne EXCELLEMMENT!")
            print("Les réponses sont intelligentes, détaillées et engageantes.")
        elif bon >= total * 0.5:
            print("✅ BON! Ollama Advanced Permissions fonctionne correctement.")
            print("Les réponses sont correctes mais peuvent être améliorées.")
        else:
            print("⚠️ À AMÉLIORER. Ollama Advanced Permissions a besoin de tweaks.")
            print("Vérifiez la température et les paramètres dans ollama_advanced_config.py")
        
        # Recommandations
        print(f"\n{'─'*70}")
        print("💡 RECOMMANDATIONS")
        print(f"{'─'*70}\n")
        
        if avg_length < 300:
            print("► Les réponses sont trop courtes")
            print("  Augmentez num_predict de 500 à 800 dans ollama_advanced_config.py")
        
        if court > total * 0.3:
            print("► Trop de réponses courtes")
            print("  Augmentez température de 0.4 à 0.6")
        
        if moyen + court > total * 0.5:
            print("► La qualité globale peut s'améliorer")
            print("  Testez les 3 modes séparément pour identification")
        
        # Sauvegarder le rapport
        self.save_report()
    
    def save_report(self):
        """Sauvegarder le rapport en JSON"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'total_tests': len(self.results),
            'results': self.results
        }
        
        filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Rapport sauvegardé: {filename}")

def main():
    runner = YAFITestRunner()
    runner.run_full_test()

if __name__ == "__main__":
    main()
