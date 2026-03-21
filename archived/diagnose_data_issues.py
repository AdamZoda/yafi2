#!/usr/bin/env python3
"""
🔧 YAFI Diagnostic - Vérifier pourquoi Ollama ne traite pas bien les données
"""

import os
import sys
import json
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def diagnose_issue(question):
    """Diagnostic complet d'une question"""
    
    print_section(f"🔍 DIAGNOSTIC: {question}")
    
    # ════════════════════════════════════════════════════════════════════════
    # DIAGNOSTIC 1: Recherche Vectorielle
    # ════════════════════════════════════════════════════════════════════════
    print("DIAGNOSTIC 1️⃣ : RECHERCHE VECTORIELLE")
    print("─" * 80)
    
    try:
        from vector_knowledge import VectorKnowledge
        
        vk = VectorKnowledge()
        results = vk.search(question, top_k=5)
        
        print(f"❓ Question: '{question}'")
        print(f"📊 Résultats trouvés: {len(results)}\n")
        
        if not results:
            print("⚠️ PROBLÈME 1: AUCUNE DONNÉE TROUVÉE!")
            print("   La recherche vectorielle ne trouve rien.")
            print("   Cela signifie que:")
            print("   - L'index FAISS est vide, OU")
            print("   - La question n'a aucune similarité avec les données\n")
            return None
        
        # Afficher les résultats
        for i, (score, content) in enumerate(results, 1):
            print(f"   [{i}] Score: {score:.3f} - {content[:80]}...")
        
        print(f"\n✅ Données trouvées: OUI")
        
        # Vérifier si les scores sont assez élevés
        avg_score = sum(score for score, _ in results) / len(results)
        print(f"   Score moyen: {avg_score:.3f}")
        
        if avg_score < 0.3:
            print(f"   ⚠️ PROBLÈME: Les scores sont trop bas!")
            print(f"   Les données trouvées ne sont probablement pas pertinentes.")
        
        context = "\n".join([content for _, content in results])
        return context
        
    except Exception as e:
        print(f"❌ ERREUR recherche: {e}")
        return None
    
    # ════════════════════════════════════════════════════════════════════════
    # DIAGNOSTIC 2: Prompt Construction
    # ════════════════════════════════════════════════════════════════════════
    print("\n\nDIAGNOSTIC 2️⃣ : CONSTRUCTION DU PROMPT")
    print("─" * 80)
    
    try:
        if not context:
            print("❌ PROBLÈME 2: PAS DE CONTEXTE!")
            print("   Le contexte est vide, donc Ollama n'a aucune donnée à utiliser.")
            return
        
        # Vérifier la taille du contexte
        print(f"✅ Contexte disponible: {len(context)} caractères\n")
        
        if len(context) < 100:
            print("⚠️ PROBLÈME 2a: LE CONTEXTE EST TROP COURT!")
            print(f"   Seulement {len(context)} caractères.")
            print("   Ollama n'a pas assez de données pour générer une bonne réponse.\n")
        
        # Montrer un extrait du prompt
        system_msg = "Tu es un assistant d'orientation scolaire."
        full_prompt = f"{system_msg}\n\nCONTEXTE:\n{context}\n\nQUESTION: {question}\n\nRÉPONSE:"
        
        print(f"Extrait du prompt envoyé à Ollama:")
        print(f"┌─ {'─'*76}┐")
        for i, line in enumerate(full_prompt.split('\n')[:10]):
            print(f"│ {line:<76} │")
        print(f"└─ {'─'*76}┘\n")
        
        print(f"Length total du prompt: {len(full_prompt)} caractères")
        
    except Exception as e:
        print(f"❌ ERREUR prompt: {e}")

def main():
    print_section("🔧 YAFI - DIAGNOSTIC DES DONNÉES")
    
    problematic_questions = [
        "comment cv",
        "bonjour",
        "hello",
        "quoi",
        "Comment choisir une école?"  # Question correcte pour comparaison
    ]
    
    print("Questions à diagnostiquer:\n")
    for i, q in enumerate(problematic_questions, 1):
        print(f"  {i}. {q}")
    
    print("\n" + "─"*80 + "\n")
    
    choice = input("Quelle question diagnostiquer? (1-5) [ou 'tous' pour tout]: ").strip()
    
    if choice.lower() == 'tous':
        for question in problematic_questions:
            diagnose_issue(question)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(problematic_questions):
                diagnose_issue(problematic_questions[idx])
            else:
                print("❌ Numéro invalide")
        except ValueError:
            print("❌ Entrée invalide")
    
    # ════════════════════════════════════════════════════════════════════════
    # RECOMMENDATIONS
    # ════════════════════════════════════════════════════════════════════════
    print_section("💡 SOLUTIONS RECOMMANDÉES")
    
    print("""
1. 🔍 AMÉLIORER LA RECHERCHE VECTORIELLE:
   - Utiliser "top_k=5" au lieu de "top_k=3"
   - Abaisser le seuil de similarité
   - Améliorer les données initiales dans la base
   
2. 📝 AMÉLIORER LES PROMPTS:
   - Forcer Ollama à utiliser le contexte
   - Ajouter "Utilisez UNIQUEMENT les donnees fournies"
   - Ajouter un système de fallback
   
3. 🧠 AMÉLIORER LES PARAMÈTRES OLLAMA:
   - Réduire la température (0.1 au lieu de 0.3)
   - Augmenter le nombre de tokens générés
   - Ajouter des stop tokens
   
4. 📊 AMÉLIORER LES DONNÉES:
   - Augmenter la taille de la base de données
   - Ajouter plus de variantes de questions
   - Indexer les synonymes
    """)

if __name__ == "__main__":
    main()
