"""
Enhanced RAG Integration with Ollama
Combines vector search, conversation history, and LLM generation
"""

import os
from typing import Optional, Dict, List
from vector_knowledge import VectorKnowledgeBase
from llm_engine import llm_engine
from prompt_engine import YAFIPromptEngine
from conversation_manager import conversation_manager

class EnhancedRAGSystem:
    """Integrates vector search with Ollama for intelligent responses"""
    
    def __init__(self):
        self.vector_kb = None
        self.min_similarity = 0.30  # Balanced for 5GB
        self.context_chunks = 6
        
        # Try to initialize vector KB
        try:
            self.vector_kb = VectorKnowledgeBase()
            if self.vector_kb.service:
                print("Enhanced RAG System initialized")
            else:
                print("Vector KB not available, RAG will be degraded")
        except Exception as e:
            print(f"RAG initialization warning: {e}")
    
    def generate_response(
        self,
        user_query: str,
        session_id: str = "default",
        use_llm: bool = True,
        temperature: float = 0.3,
        profile: Optional[Dict] = None
    ) -> Dict:
        """Standard non-streaming version"""
        history = (profile.get('history')[-5:] if profile else None) or conversation_manager.get_history(session_id, 3)
        search_results = self.vector_kb.search(user_query, self.context_chunks, self.min_similarity) if self.vector_kb else None
        
        prompt = YAFIPromptEngine.build_prompt(user_query, search_results or [], history, profile)
        llm_response = llm_engine.ask(prompt, temperature=temperature)
        
        if llm_response:
            resp = YAFIPromptEngine.format_response(llm_response, search_results, True)
            return {"response": resp, "method": "rag_llm", "confidence": 0.8}
        return {"response": "Erreur LLM", "method": "error"}

    def generate_response_stream(
        self,
        user_query: str,
        session_id: str = "default",
        temperature: float = 0.3,
        profile: Optional[Dict] = None
    ):
        """
        Streamed response generation
        Yields:
            String chunks
        """
        try:
            # 1. Vector search
            search_results = None
            if self.vector_kb and self.vector_kb.service:
                search_results = self.vector_kb.search(
                    user_query,
                    top_k=self.context_chunks,
                    threshold=self.min_similarity
                )
            
            # 2. Get history
            history = (profile.get('history')[-5:] if profile else None) or conversation_manager.get_history(session_id, 3)
            
            # 3. Guardrail: If no results or very low quality, don't let LLM hallucinate
            if not search_results or len(search_results) == 0:
                print(f"  RAG Guardrail: No context found for '{user_query}'. Returning fallback.")
                yield YAFIPromptEngine.FALLBACK_RESPONSE
                return

            # 3b. City-mismatch guardrail
            CITIES = ["fes", "fès", "marrakech", "tanger", "agadir", "oujda", "kenitra", "meknes", "meknès", "tetouan", "settat", "eljadida", "beni mellal", "safi", "nador"]
            query_low = user_query.lower()
            user_city = None
            for city in CITIES:
                if city in query_low:
                    user_city = city
                    break
            
            if user_city:
                # Check if any retrieved context mentions this city
                context_text = " ".join([r['text'].lower() for r in search_results])
                if user_city not in context_text and user_city.replace("è", "e") not in context_text:
                    print(f"  RAG City-Mismatch: User asked about '{user_city}' but context has no data.")
                    yield f"⚠️ Ma base de connaissances ne contient pas encore d'information spécifique sur les universités de **{user_city.capitalize()}**.\n\nVoici ce que j'ai trouvé de plus proche :\n\n"

            # 4. Build prompt
            prompt = YAFIPromptEngine.build_prompt(
                query=user_query,
                search_results=search_results,
                history=history,
                profile=profile
            )
            
            # 5. Stream from Ollama
            full_response = ""
            for chunk in llm_engine.ask_stream(prompt, temperature=temperature):
                full_response += chunk
                yield chunk
            
            # 6. Yield citations at the end
            if search_results:
                citations = YAFIPromptEngine.add_source_citations("", search_results)
                if citations.strip():
                    yield "\n" + citations

        except Exception as e:
            print(f"RAG Stream Error: {e}")
            yield f"\n[Erreur RAG: {str(e)}]"
    
    def get_fallback_response(self) -> str:
        """Get a fallback response when RAG fails"""
        return YAFIPromptEngine.FALLBACK_RESPONSE
    
    def health_check(self) -> Dict:
        """Check system health"""
        return {
            "vector_kb_available": self.vector_kb is not None and self.vector_kb.service is not None,
            "llm_available": llm_engine.provider is not None,
            "llm_health": llm_engine.health_check()
        }

# Singleton instance
rag_system = EnhancedRAGSystem()
