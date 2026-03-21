"""
Enhanced Prompting System for YAFI
Strict prompts to prevent hallucinations and ensure accurate responses
"""

from typing import Dict, List, Optional


class YAFIPromptEngine:
    """Manages prompts and response formatting for YAFI chatbot"""
    
    SYSTEM_PROMPT = """Tu es YAFI, assistant d'orientation scolaire au Maroc. 🎓
Réponds en français, de façon structurée avec des emojis.

PROFIL: {profile_context}

CONTEXTE: {context}

HISTORIQUE: {history}

QUESTION: {query}

RÉPONSE:"""

    FALLBACK_RESPONSE = """❌ **Information non disponible**

Je n'ai pas trouvé d'information fiable dans ma base de connaissances pour répondre à cette question.

**Suggestions** :
- Reformulez votre question différemment
- Posez une question plus spécifique
- Consultez directement les sites officiels :
  • www.men.gov.ma (Ministère de l'Éducation)
  • www.tawjihi.ma (Orientation post-bac)
  • www.cnc.ma (Concours écoles d'ingénieurs)

💬 Puis-je vous aider avec autre chose ?"""

    NO_CONTEXT_PROMPT = """Tu es YAFI, un assistant d'orientation académique pour les étudiants marocains.

L'utilisateur a posé une question pour laquelle tu n'as pas de contexte spécifique.

RÈGLES :
1. Réponds de manière générale et utile
2. Suggère des ressources officielles
3. Propose de reformuler la question
4. Reste dans ton domaine (orientation académique Maroc)

HISTORIQUE :
{history}

QUESTION :
{query}

RÉPONSE :"""

    @staticmethod
    def format_context(search_results: List[Dict]) -> str:
        """
        Format search results into context for LLM
        
        Args:
            search_results: List of search results with chunks and scores
            
        Returns:
            Formatted context string
        """
        if not search_results:
            return "Aucun contexte disponible."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            category = result['metadata'].get('category', 'Général')
            text = result['text'][:300]  # Truncate for speed with small model
            score = result['score']
            
            context_parts.append(
                f"[Source {i} - {category} - {score:.0%}]\n{text}"
            )
        
        return "\n\n---\n\n".join(context_parts)
    
    @staticmethod
    def format_history(history: List[Dict], max_exchanges: int = 2) -> str:
        """
        Format conversation history for context
        
        Args:
            history: List of conversation messages
            max_exchanges: Maximum number of exchanges to include
            
        Returns:
            Formatted history string
        """
        if not history:
            return "Aucun historique."
        
        # Get last N exchanges (user + assistant pairs)
        recent = history[-(max_exchanges * 2):]
        
        formatted = []
        for msg in recent:
            role = "Utilisateur" if msg['role'] == 'user' else "Assistant"
            # Handle both 'content' and 'text' keys for robustness
            content = msg.get('content') or msg.get('text') or ""
            content = content[:200]  # Truncate long messages
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def add_source_citations(response: str, search_results: List[Dict]) -> str:
        """
        Add source citations to the response
        
        Args:
            response: Generated response
            search_results: Search results used for context
            
        Returns:
            Response with citations
        """
        if not search_results:
            return response
        
        # Extract unique categories
        categories = list(set(
            r['metadata'].get('category', 'Général') 
            for r in search_results
        ))
        
        # Add citations
        citations = f"\n\n📚 **Sources** : {', '.join(categories)}"
        
        # Add confidence indicator
        avg_score = sum(r['score'] for r in search_results) / len(search_results)
        
        if avg_score >= 0.8:
            confidence = "🟢 Confiance élevée"
        elif avg_score >= 0.6:
            confidence = "🟡 Confiance moyenne"
        else:
            confidence = "🟠 Confiance faible"
        
        citations += f"\n{confidence} ({avg_score:.0%})"
        
        return response + citations
    
    @classmethod
    def build_prompt(
        cls,
        query: str,
        search_results: Optional[List[Dict]] = None,
        history: Optional[List[Dict]] = None,
        profile: Optional[Dict] = None
    ) -> str:
        """
        Build complete prompt for LLM
        
        Args:
            query: User query
            search_results: Search results for context
            history: Conversation history
            
        Returns:
            Complete formatted prompt
        """
        # Build profile summary
        profile_context = "Aucune information de profil encore."
        if profile:
            profile_context = f"Bac: {profile.get('bac', '?')}, Moyenne: {profile.get('moyenne', '?')}, Ville: {profile.get('ville', '?')}, Budget: {profile.get('budget', '?')}"
            if profile.get('interets'):
                profile_context += f", Intérêts: {', '.join(profile['interets'])}"

        if search_results:
            # Use strict prompt with context
            context = cls.format_context(search_results)
            history_text = cls.format_history(history or [])
            
            return cls.SYSTEM_PROMPT.format(
                profile_context=profile_context,
                context=context,
                history=history_text,
                query=query
            )
        else:
            # Use fallback prompt without context
            history_text = cls.format_history(history or [])
            
            # For simplicity, we can reuse SYSTEM_PROMPT with empty context or fallback
            return cls.NO_CONTEXT_PROMPT.format(
                history=history_text,
                query=query
            )
    
    @classmethod
    def format_response(
        cls,
        response: str,
        search_results: Optional[List[Dict]] = None,
        add_citations: bool = True
    ) -> str:
        """
        Format final response with citations
        
        Args:
            response: Raw LLM response
            search_results: Search results used
            add_citations: Whether to add source citations
            
        Returns:
            Formatted response
        """
        if not response:
            return cls.FALLBACK_RESPONSE
        
        if add_citations and search_results:
            response = cls.add_source_citations(response, search_results)
        
        return response


if __name__ == "__main__":
    # Test the prompt engine
    print("🧪 Testing YAFI Prompt Engine\n")
    
    # Mock search results
    mock_results = [
        {
            'text': "L'ENSA est une école d'ingénieurs publique...",
            'metadata': {'category': 'Écoles', 'question': "C'est quoi l'ENSA ?"},
            'score': 0.92
        },
        {
            'text': "Pour s'inscrire à l'ENSA, il faut passer le concours CNC...",
            'metadata': {'category': 'Admissions', 'question': 'Concours ENSA'},
            'score': 0.85
        }
    ]
    
    # Mock history
    mock_history = [
        {'role': 'user', 'content': "C'est quoi l'ENSA ?"},
        {'role': 'assistant', 'content': "L'ENSA est une école..."}
    ]
    
    # Build prompt
    prompt = YAFIPromptEngine.build_prompt(
        query="Comment s'inscrire ?",
        search_results=mock_results,
        history=mock_history
    )
    
    print("📝 Generated Prompt:")
    print("-" * 60)
    print(prompt[:500] + "...")
    print("-" * 60)
    
    # Format response
    mock_response = "Pour s'inscrire à l'ENSA, vous devez passer le concours CNC..."
    formatted = YAFIPromptEngine.format_response(mock_response, mock_results)
    
    print("\n✅ Formatted Response:")
    print("-" * 60)
    print(formatted)
    print("-" * 60)
