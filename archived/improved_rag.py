#!/usr/bin/env python3
"""
🚀 YAFI - Version Améliorée du Prompt Engine
Force Ollama à mieux utiliser les données
"""

import os
from pathlib import Path

class ImprovedPromptEngine:
    """Version améliorée du prompt engine pour mieux utiliser les données"""
    
    SYSTEM_PROMPT = """Tu es YAFI, un assistant expert en orientation scolaire.

⚠️ INSTRUCTIONS CRITIQUES:
1. Tu DOIS utiliser UNIQUEMENT les informations fournies dans la section CONTEXTE
2. Si une information n'est pas dans le CONTEXTE, dis: "Je n'ai pas cette information"
3. Sois direct, concis et pratique
4. Structure ta réponse avec des numéros ou bullets
5. Cite toujours la source de tes informations

CONTEXTE = ta seule source de vérité. Suis-le strictement.
"""

    FALLBACK_PROMPT = """Tu es YAFI, assistant d'orientation scolaire.
La question "{question}" ne correspond à aucune donnée dans ma base.

Réponds poliment:
- Reformule la question pour en chercher une proche
- Suggère des questions alternatives
- Offre d'aider autrement
"""

    @staticmethod
    def build_effective_prompt(question: str, context: str, top_results_count: int = 3) -> str:
        """
        Construire un prompt plus efficace pour Ollama
        
        Args:
            question: La question de l'utilisateur
            context: Le contenu retrouvé dans la base de données
            top_results_count: Nombre de résultats utilisés
            
        Returns:
            Le prompt formé pour Ollama
        """
        
        if not context or len(context.strip()) < 50:
            # Pas assez de contexte
            return ImprovedPromptEngine.FALLBACK_PROMPT.format(question=question)
        
        # Prompt efficace avec instructions strictes
        prompt = f"""{ImprovedPromptEngine.SYSTEM_PROMPT}

════════════════════════════════════════════════════════════
CONTEXTE (Information de la base de données):
════════════════════════════════════════════════════════════

{context}

════════════════════════════════════════════════════════════
QUESTION DE L'UTILISATEUR:
════════════════════════════════════════════════════════════

{question}

════════════════════════════════════════════════════════════
TA RÉPONSE (Basée UNIQUEMENT sur le contexte):
════════════════════════════════════════════════════════════

✓ Structure ta réponse:
✓ Sois spécifique et pragmatique
✓ Utilise les données du contexte comme base
✓ Ajoute des numéros ou des pointeurs pour la clarté

RÉPONSE:"""
        
        return prompt
    
    @staticmethod
    def build_with_quality_boost(question: str, context: str, retrieval_scores: list = None) -> tuple:
        """
        Construire un prompt avec boost de qualité
        
        Returns:
            (prompt, temperature) - Le prompt et la température recommandée
        """
        
        # Ajuster la température basée sur la qualité du contexte
        if retrieval_scores and len(retrieval_scores) > 0:
            avg_score = sum(retrieval_scores) / len(retrieval_scores)
            
            # Scores bas = contexte peu pertinent = réponse plus déterministe
            if avg_score < 0.4:
                temperature = 0.1  # Très déterministe
            elif avg_score < 0.6:
                temperature = 0.2  # Modérément déterministe
            else:
                temperature = 0.3  # Créatif mais focalisé
        else:
            temperature = 0.3
        
        prompt = ImprovedPromptEngine.build_effective_prompt(question, context)
        return prompt, temperature

class ImprovedRAG:
    """RAG amélioré pour meilleures réponses"""
    
    @staticmethod
    def generate_response_improved(question: str, conversation_id: str, 
                                  conversation_manager=None) -> str:
        """
        Générer une réponse améliorée
        """
        try:
            from vector_knowledge import VectorKnowledge
            from llm_engine import llm_engine
            import requests
            
            # 1️⃣ Recherche améliorée (top_k augmenté)
            vk = VectorKnowledge()
            results = vk.search(question, top_k=5)  # Augmenté de 3 à 5
            
            if not results:
                return "Je n'ai pas trouvé d'informations pertinentes. Pouvez-vous reformuler votre question?"
            
            # Extraire scores et contexte
            scores = [score for score, _ in results]
            context = "\n\n".join([content for _, content in results])
            
            # 2️⃣ Construire prompt amélioré
            prompt, temperature = ImprovedPromptEngine.build_with_quality_boost(
                question, 
                context, 
                scores
            )
            
            # 3️⃣ Générer avec Ollama amélioré
            ollama_url = os.environ.get('OLLAMA_HOST', 'http://localhost:11435')
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "num_predict": 500  # Limiter la longueur
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '').strip()
                
                # Nettoyer les artefacts
                answer = ImprovedRAG.clean_response(answer)
                
                return answer
            else:
                return "Erreur lors de la génération de la réponse."
                
        except Exception as e:
            print(f"❌ Erreur RAG amélioré: {e}")
            return "Erreur lors du traitement de votre question."
    
    @staticmethod
    def clean_response(response: str) -> str:
        """Nettoyer la réponse d'Ollama"""
        
        # Enlever les répétitions
        lines = response.split('\n')
        unique_lines = []
        for line in lines:
            if line.strip() and line.strip() not in [l.strip() for l in unique_lines]:
                unique_lines.append(line)
        
        response = '\n'.join(unique_lines)
        
        # Enlever les prefixes inutiles
        for prefix in ["RÉPONSE:", "Response:", "Je réponds:"]:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        return response.strip()

# ════════════════════════════════════════════════════════════════════════
# EXEMPLE D'UTILISATION
# ════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 YAFI Improved RAG System\n")
    
    # Test des questions problématiques
    test_questions = [
        "Quelle est la meilleure école d'informatique?",
        "Comment choisir son orientation?",
        "comment cv"  # Question vague
    ]
    
    from conversation_manager import ConversationManager
    
    rag = ImprovedRAG()
    conv_mgr = ConversationManager()
    
    for question in test_questions:
        print(f"\n{'='*70}")
        print(f"❓ Question: {question}")
        print(f"{'='*70}")
        
        response = ImprovedRAG.generate_response_improved(
            question, 
            "test_session",
            conv_mgr
        )
        
        print(f"\n✅ Réponse:")
        print(response)
        print()
