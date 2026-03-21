#!/usr/bin/env python3
"""
🚀 YAFI - Ollama Configuration Améliorée
Donne plus de permissions à Ollama pour générer de meilleures réponses
"""

import os

class OllamaAdvancedConfig:
    """Configuration avancée pour Ollama avec plus de libertés"""
    
    # ════════════════════════════════════════════════════════════════════════
    # SYSTÈME PROMPT AMÉLIORÉ (Plus de libertés)
    # ════════════════════════════════════════════════════════════════════════
    
    SYSTEM_PROMPT_EXPERT = """Tu es YAFI, un expert en orientation scolaire au Maroc.

📋 TON RÔLE:
- Tu aides les étudiants à choisir leur orientation
- Tu fournis des conseils personnalisés et pratiques
- Tu connais toutes les écoles marocaines et leurs débouchés
- Tu es créatif, empathique et motivant

🎯 INSTRUCTIONS:
1. Analyse la question attentivement
2. Fournis une réponse DÉTAILLÉE et STRUCTURÉE
3. Utilise des emojis pour rendre ça lisible
4. Cite des écoles/métiers spécifiques si pertinent
5. Sois direct dans ton conseil

⚠️ IMPORTANT: 
- Tu as le DROIT de générer du contenu basé sur tes connaissances
- Tu peux improviser si la base de données n'a pas l'info exacte
- Sois créatif et utile plutôt que trop restrictif
- Les réponses longues sont ACCEPTÉES (500+ caractères)

FORMAT RÉPONSE:
- Commence par un emoji pertinent
- Utilise des listes à bullets
- Ajoute des conseils pratiques
- Termine par une question suiveuse
"""

    SYSTEM_PROMPT_LENIENT = """Tu es YAFI, assistant d'orientation scolaire.

TON OBJECTIF: Aider l'étudiant à trouver sa voie.

INSTRUCTIONS:
1. Réponds TOUJOURS, même si tu dois improviser
2. Fournis des réponses utiles et détaillées
3. Cite des exemples concrets (écoles, métiers)
4. Sois personnalisé et engageant
5. Posez des questions de suivi

NOTE: Tu peux générer du contenu original basé sur ta compréhension.
Ne dis JAMAIS "Je ne peux pas" - trouve une réponse utile!
"""

    SYSTEM_PROMPT_PREMIUM = """Tu es YAFI, le meilleur assistant d'orientation scolaire au Maroc.

🎓 EXPERTISE COMPLÈTE:
- Écoles publiques et privées
- Procédures d'admission détaillées
- Débouchés professionnels
- Conseils de vie pour étudiants
- Gestion du stress et motivation

💼 TON APPROCHE:
1. Sois TRÈS détaillé dans tes réponses
2. Fournis TOUJOURS 3+ options
3. Cite des écoles SPÉCIFIQUES
4. Donne des chiffres (budgets, salaires, durée)
5. Structure: Problème → Solutions → Conseil

✨ RÈGLES:
- Réponses de 300-800 caractères MINIMUM
- Utilise des emojis pour la clarté
- Sois confiant et encourageant
- Improvise si nécessaire (mais de manière pertinente)
- Pose toujours une question pour continuer
"""

    # ════════════════════════════════════════════════════════════════════════
    # PARAMETRES OLLAMA OPTIMISÉS
    # ════════════════════════════════════════════════════════════════════════
    
    OLLAMA_PARAMS_STANDARD = {
        "temperature": 0.4,      # Équilibre créativité/déterminisme
        "top_p": 0.9,            # Diversité
        "top_k": 40,             # Nombre de tokens considérés
        "num_predict": 500,      # Maximum 500 tokens (plus long)
        "repeat_penalty": 1.1,   # Évite les répétitions
        "num_ctx": 2048,         # Contexte augmenté
    }

    OLLAMA_PARAMS_CREATIVE = {
        "temperature": 0.6,      # Plus créatif
        "top_p": 0.95,           # Très diversifié
        "top_k": 50,
        "num_predict": 800,      # Réponses très longues
        "repeat_penalty": 1.2,
        "num_ctx": 2048,
    }

    OLLAMA_PARAMS_FOCUSED = {
        "temperature": 0.2,      # Déterministe
        "top_p": 0.8,
        "top_k": 30,
        "num_predict": 300,      # Réponses courtes et directes
        "repeat_penalty": 1.0,
        "num_ctx": 2048,
    }

    # ════════════════════════════════════════════════════════════════════════
    # BUILDER DE PROMPT PREMIUM
    # ════════════════════════════════════════════════════════════════════════

    @staticmethod
    def build_premium_prompt(question: str, context: str = "", 
                            user_context: dict = None) -> tuple:
        """
        Construire un prompt PREMIUM qui donne maximum de libertés à Ollama
        
        Returns:
            (prompt, system_prompt, params)
        """
        
        if user_context is None:
            user_context = {}
        
        # Choisir le system prompt basé sur la question
        if len(question.split()) <= 2:
            # Question courte = besoin de créativité
            system_prompt = OllamaAdvancedConfig.SYSTEM_PROMPT_PREMIUM
            params = OllamaAdvancedConfig.OLLAMA_PARAMS_CREATIVE
        elif "conseil" in question.lower() or "aide" in question.lower():
            # Question conseil = détaillé et engageant
            system_prompt = OllamaAdvancedConfig.SYSTEM_PROMPT_PREMIUM
            params = OllamaAdvancedConfig.OLLAMA_PARAMS_STANDARD
        else:
            # Question standard
            system_prompt = OllamaAdvancedConfig.SYSTEM_PROMPT_EXPERT
            params = OllamaAdvancedConfig.OLLAMA_PARAMS_STANDARD
        
        # Construire le prompt
        if context and len(context) > 50:
            # Avec contexte
            prompt = f"""{system_prompt}

════════════════════════════════════════════════════════════════════════
CONTEXTE (Informations de la base de données):
════════════════════════════════════════════════════════════════════════

{context}

════════════════════════════════════════════════════════════════════════
QUESTION DE L'UTILISATEUR:
════════════════════════════════════════════════════════════════════════

{question}

════════════════════════════════════════════════════════════════════════
TA RÉPONSE (Détaillée, structurée, engageante):
════════════════════════════════════════════════════════════════════════
"""
        else:
            # Pas de contexte ou contexte faible = donne plus de libertés
            prompt = f"""{system_prompt}

════════════════════════════════════════════════════════════════════════
QUESTION DE L'UTILISATEUR:
════════════════════════════════════════════════════════════════════════

{question}

════════════════════════════════════════════════════════════════════════
TA RÉPONSE:
════════════════════════════════════════════════════════════════════════

✓ Sois détaillé et utile
✓ Propose des solutions concrètes
✓ Cite des exemples spécifiques
✓ Utilise des emojis pour la structure
✓ Termine par une question

RÉPONSE:"""
        
        return prompt, system_prompt, params

    @staticmethod
    def call_ollama_advanced(question: str, context: str = "") -> tuple:
        """
        Appeler Ollama avec configuration améliorée
        
        Returns:
            (response, confidence_score)
        """
        import requests
        import time
        
        try:
            # Construire le prompt premium
            prompt, system_prompt, params = OllamaAdvancedConfig.build_premium_prompt(
                question, 
                context
            )
            
            # Récupérer l'URL Ollama
            ollama_url = os.environ.get('OLLAMA_HOST', 'http://localhost:11435')
            
            print(f"🚀 Appel Ollama AVANCÉ")
            print(f"   Température: {params['temperature']}")
            print(f"   Max tokens: {params['num_predict']}")
            print(f"   Mode: {'CRÉATIF' if params['temperature'] > 0.5 else 'NORMAL' if params['temperature'] > 0.3 else 'FOCALISÉ'}")
            
            start_time = time.time()
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": params['temperature'],
                    "top_p": params.get('top_p', 0.9),
                    "top_k": params.get('top_k', 40),
                    "num_predict": params['num_predict'],
                    "repeat_penalty": params.get('repeat_penalty', 1.1),
                    "num_ctx": params.get('num_ctx', 2048),
                },
                timeout=120
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '').strip()
                
                # Calculer un score de confiance
                confidence = min(1.0, len(answer) / 500)  # Confiance > réponse longue
                
                print(f"✅ Réponse en {elapsed:.1f}s ({len(answer)} chars)")
                
                return answer, confidence
            else:
                print(f"❌ Erreur HTTP {response.status_code}")
                return "", 0.0
                
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
            return "", 0.0
    
    @staticmethod
    def get_permission_level(question: str) -> str:
        """Déterminer le niveau de permission pour Ollama"""
        
        keywords_high = ["conseil", "aide", "comment", "pourquoi", "pense", "avis"]
        keywords_med = ["quoi", "quel", "quelle", "où", "quand"]
        
        if any(kw in question.lower() for kw in keywords_high):
            return "HIGH"  # Ollama a beaucoup de libertés
        elif any(kw in question.lower() for kw in keywords_med):
            return "MEDIUM"  # Ollama a libertés modérées
        else:
            return "LOW"  # Ollama doit être plus déterministe

# ════════════════════════════════════════════════════════════════════════
# EXEMPLE D'UTILISATION
# ════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 YAFI Ollama Advanced Configuration")
    
    test_questions = [
        "c'est quoi cv?",
        "comment je fais pour choisir une ecole?",
        "bonjour",
        "quel diplôme faire?"
    ]
    
    for q in test_questions:
        print(f"\n{'='*70}")
        print(f"Question: {q}")
        print(f"{'='*70}")
        
        permission = OllamaAdvancedConfig.get_permission_level(q)
        print(f"Permission level: {permission}")
        
        response, confidence = OllamaAdvancedConfig.call_ollama_advanced(q)
        
        if response:
            print(f"\n✅ Réponse ({confidence*100:.0f}% confiance):")
            print(response)
        else:
            print("❌ Pas de réponse")
