#!/usr/bin/env python3
"""
🧪 YAFI Complete System Test
Teste Ollama + Backend + RAG + Base de Données
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# Ajouter le répertoire backend au Python path
sys.path.insert(0, str(Path(__file__).parent))

class YAFISystemTester:
    def __init__(self):
        self.results = []
        self.ollama_url = "http://localhost:11435"
        self.backend_url = "http://localhost:5000"
        
    def print_header(self, title):
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    
    def print_section(self, title):
        print(f"\n{'─'*70}")
        print(f"  {title}")
        print(f"{'─'*70}\n")
    
    def test_ollama_connection(self):
        """Test 1: Connexion à Ollama"""
        self.print_section("TEST 1️⃣ : CONNEXION À OLLAMA")
        
        try:
            print(f"🔍 Tentative de connexion à {self.ollama_url}...")
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                print(f"✅ SUCCÈS: Ollama répond correctement")
                print(f"📦 Modèles disponibles: {len(models)}")
                
                for model in models:
                    print(f"   - {model['name']}")
                
                self.results.append(("Ollama Connection", "✅ PASS"))
                return True
            else:
                print(f"❌ ERREUR: Code HTTP {response.status_code}")
                self.results.append(("Ollama Connection", "❌ FAIL"))
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ ERREUR: Impossible de se connecter à Ollama")
            print(f"   Assurez-vous que Ollama est lancé sur port 11435")
            print(f"   Commande: set OLLAMA_HOST=0.0.0.0:11435 && ollama serve")
            self.results.append(("Ollama Connection", "❌ FAIL"))
            return False
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.results.append(("Ollama Connection", "❌ FAIL"))
            return False
    
    def test_ollama_generation(self):
        """Test 2: Génération avec Ollama"""
        self.print_section("TEST 2️⃣ : GÉNÉRATION OLLAMA")
        
        if not self._is_ollama_running():
            print("⏭️  Skipped (Ollama not running)")
            return False
        
        try:
            print("🤖 Test de génération simple...")
            prompt = "Quelle est l'importance de l'orientation scolaire?"
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                generated = data.get('response', '').strip()
                
                if generated:
                    print(f"✅ SUCCÈS: Ollama a généré une réponse")
                    print(f"\n📝 Prompt: {prompt}")
                    print(f"\n💬 Réponse (premiers 200 chars):")
                    print(f"   {generated[:200]}...")
                    print(f"\n📊 Longueur: {len(generated)} caractères")
                    
                    self.results.append(("Ollama Generation", "✅ PASS"))
                    return True
                else:
                    print(f"❌ ERREUR: Réponse vide")
                    self.results.append(("Ollama Generation", "❌ FAIL"))
                    return False
            else:
                print(f"❌ ERREUR: Code HTTP {response.status_code}")
                self.results.append(("Ollama Generation", "❌ FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.results.append(("Ollama Generation", "❌ FAIL"))
            return False
    
    def test_vector_search(self):
        """Test 3: Recherche vectorielle"""
        self.print_section("TEST 3️⃣ : RECHERCHE VECTORIELLE (FAISS)")
        
        try:
            from vector_knowledge import VectorKnowledge
            
            print("🔎 Charger l'index vectoriel...")
            vk = VectorKnowledge()
            
            if not vk.index:
                print("❌ ERREUR: Index vectoriel non chargé")
                self.results.append(("Vector Search", "❌ FAIL"))
                return False
            
            print(f"✅ Index chargé: {vk.index.ntotal} documents")
            
            # Test de recherche
            query = "orientation scolaire"
            print(f"\n🔍 Recherche pour: '{query}'")
            
            results = vk.search(query, top_k=3)
            
            if results:
                print(f"✅ SUCCÈS: Trouvé {len(results)} résultats")
                for i, (score, content) in enumerate(results, 1):
                    print(f"\n   [{i}] Score: {score:.2f}")
                    print(f"       {content[:100]}...")
                
                self.results.append(("Vector Search", "✅ PASS"))
                return True
            else:
                print(f"⚠️  AVERTISSEMENT: Aucun résultat trouvé")
                self.results.append(("Vector Search", "⚠️ WARNING"))
                return False
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.results.append(("Vector Search", "❌ FAIL"))
            return False
    
    def test_enhanced_rag(self):
        """Test 4: Système RAG complet"""
        self.print_section("TEST 4️⃣ : SYSTÈME RAG (RETRIEVAL-AUGMENTED GENERATION)")
        
        if not self._is_ollama_running():
            print("⏭️  Skipped (Ollama not running)")
            return False
        
        try:
            from enhanced_rag import EnhancedRAGSystem
            from conversation_manager import ConversationManager
            
            print("🧠 Initialiser le système RAG...")
            rag = EnhancedRAGSystem()
            conv_manager = ConversationManager()
            
            # Question de test
            question = "Quelle est l'importance de bien choisir son orientation scolaire?"
            print(f"\n❓ Question: {question}")
            
            print(f"\n⏳ Génération de réponse (cela peut prendre 10-20 secondes)...")
            start_time = time.time()
            
            response = rag.generate_response(
                question=question,
                conversation_id="test_session",
                conversation_manager=conv_manager
            )
            
            elapsed = time.time() - start_time
            
            if response and response.strip():
                print(f"✅ SUCCÈS: Réponse générée en {elapsed:.1f}s")
                print(f"\n💬 Réponse RAG:")
                print(f"─" * 70)
                print(response[:500])
                if len(response) > 500:
                    print("...")
                print(f"─" * 70)
                print(f"\n📊 Longueur totale: {len(response)} caractères")
                
                # Vérifier que la réponse contient des références
                if "Source:" in response or "Basé sur" in response:
                    print("✅ La réponse contient des références à la base de données")
                else:
                    print("⚠️  La réponse ne semble pas référencer la base de données")
                
                self.results.append(("Enhanced RAG", "✅ PASS"))
                return True
            else:
                print(f"❌ ERREUR: Réponse vide")
                self.results.append(("Enhanced RAG", "❌ FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            self.results.append(("Enhanced RAG", "❌ FAIL"))
            return False
    
    def test_backend_api(self):
        """Test 5: API Backend"""
        self.print_section("TEST 5️⃣ : API BACKEND FLASK")
        
        try:
            print(f"🔍 Tentative de connexion à {self.backend_url}...")
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ SUCCÈS: Backend répond correctement")
                print(f"📊 Status: {response.json()}")
                self.results.append(("Backend API", "✅ PASS"))
                return True
            else:
                print(f"❌ ERREUR: Code HTTP {response.status_code}")
                self.results.append(("Backend API", "❌ FAIL"))
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ ERREUR: Impossible de se connecter au Backend")
            print(f"   Assurez-vous que le Backend est lancé sur port 5000")
            print(f"   Commande: cd backend && python server.py")
            self.results.append(("Backend API", "❌ FAIL"))
            return False
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.results.append(("Backend API", "❌ FAIL"))
            return False
    
    def test_complete_pipeline(self):
        """Test 6: Pipeline complet Backend->RAG->Ollama"""
        self.print_section("TEST 6️⃣ : PIPELINE COMPLET (BACKEND API)")
        
        try:
            print(f"📡 Test de l'endpoint /ask...")
            
            payload = {
                "question": "Comment choisir une école?",
                "conversation_id": "test_session"
            }
            
            response = requests.post(
                f"{self.backend_url}/ask",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                
                print(f"✅ SUCCÈS: Endpoint /ask répond correctement")
                print(f"\n❓ Question: {payload['question']}")
                print(f"\n💬 Réponse:")
                print(f"─" * 70)
                print(answer[:500])
                if len(answer) > 500:
                    print("...")
                print(f"─" * 70)
                
                self.results.append(("Complete Pipeline", "✅ PASS"))
                return True
            else:
                print(f"❌ ERREUR: Code HTTP {response.status_code}")
                print(f"   Réponse: {response.text}")
                self.results.append(("Complete Pipeline", "❌ FAIL"))
                return False
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.results.append(("Complete Pipeline", "❌ FAIL"))
            return False
    
    def _is_ollama_running(self):
        """Vérifier si Ollama est en cours d'exécution"""
        try:
            requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return True
        except:
            return False
    
    def print_summary(self):
        """Afficher le résumé des tests"""
        self.print_header("📊 RÉSUMÉ DES TESTS")
        
        print(f"{'Test':<30} {'Résultat':<20}")
        print("─" * 50)
        
        for test_name, result in self.results:
            print(f"{test_name:<30} {result:<20}")
        
        # Comptage
        passed = sum(1 for _, result in self.results if "✅" in result)
        failed = sum(1 for _, result in self.results if "❌" in result)
        warned = sum(1 for _, result in self.results if "⚠️" in result)
        
        print("─" * 50)
        print(f"\n✅ PASS: {passed}/{len(self.results)}")
        print(f"❌ FAIL: {failed}/{len(self.results)}")
        print(f"⚠️  WARN: {warned}/{len(self.results)}")
        
        # Verdict final
        print("\n" + "="*70)
        if failed == 0 and passed >= 4:
            print("🎉 SUCCÈS! Le système YAFI est prêt!")
            print("✅ Ollama + Backend + RAG + Base de données = OPÉRATIONNEL")
        elif failed <= 2:
            print("⚠️  Système partiellement fonctionnel. See errors above.")
        else:
            print("❌ Système non opérationnel. Vérifiez les erreurs ci-dessus.")
        print("="*70)
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        self.print_header("🧪 YAFI COMPLETE SYSTEM TEST")
        print("Test Ollama + Backend + RAG + Vector Database")
        print("\n⏩ Mode: Local Testing")
        print(f"🎯 Ollama URL: {self.ollama_url}")
        print(f"🎯 Backend URL: {self.backend_url}")
        
        # Tests
        self.test_ollama_connection()
        self.test_ollama_generation()
        self.test_vector_search()
        self.test_enhanced_rag()
        self.test_backend_api()
        self.test_complete_pipeline()
        
        # Summary
        self.print_summary()

if __name__ == "__main__":
    tester = YAFISystemTester()
    tester.run_all_tests()
