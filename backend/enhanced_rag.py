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
        self.min_similarity = 0.35
        self.context_chunks = 2  # Top-2 chunks for good quality + speed
        
        # Try to initialize vector KB
        try:
            self.vector_kb = VectorKnowledgeBase()
            if self.vector_kb.service:
                print("✅ Enhanced RAG System initialized")
            else:
                print("⚠️ Vector KB not available, RAG will be degraded")
        except Exception as e:
            print(f"⚠️ RAG initialization warning: {e}")
    
    def generate_response(
        self,
        user_query: str,
        session_id: str = "default",
        use_llm: bool = True,
        temperature: float = 0.3,
        profile: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a response using RAG + Ollama
        
        Args:
            user_query: User's question
            session_id: Conversation session ID
            use_llm: Whether to use Ollama for generation
            temperature: LLM creativity level
            profile: User profile context from memory
            
        Returns:
            Dict with response, confidence, sources, etc.
        """
        result = {
            "response": "",
            "confidence": 0.0,
            "sources": [],
            "method": "none",
            "error": None
        }
        
        try:
            # 1. Add user message to history (handled by server now, but keep for fallback)
            # conversation_manager.add_message(session_id, 'user', user_query)
            
            # 2. Vector search
            search_results = None
            if self.vector_kb and self.vector_kb.service:
                search_results = self.vector_kb.search(
                    user_query,
                    top_k=self.context_chunks,
                    threshold=self.min_similarity
                )
            
            # 3. Get conversation history
            # Use profile history or conversation_manager
            history = []
            if profile and profile.get('history'):
                history = profile['history'][-5:]
            else:
                history = conversation_manager.get_history(session_id, last_n=3)
            
            # 4. Build prompt
            if use_llm and llm_engine.enabled and llm_engine.provider:
                prompt = YAFIPromptEngine.build_prompt(
                    query=user_query,
                    search_results=search_results or [],
                    history=history,
                    profile=profile
                )
                
                # 5. Call Ollama
                llm_response = llm_engine.ask(prompt, temperature=temperature)
                
                if llm_response:
                    # 6. Format response with citations
                    result["response"] = YAFIPromptEngine.format_response(
                        llm_response,
                        search_results=search_results,
                        add_citations=True
                    )
                    result["method"] = "rag_llm"
                    result["confidence"] = sum(r['score'] for r in search_results) / len(search_results) if search_results else 0.0
                    result["sources"] = list(set(
                        r['metadata'].get('category', 'Général')
                        for r in search_results
                    )) if search_results else []
                else:
                    # LLM failed, use direct context
                    result["response"] = "\n\n".join(
                        [r['text'] for r in search_results[:2]]
                    )
                    result["method"] = "rag_fallback"
                    result["confidence"] = search_results[0]['score']
                    result["sources"] = [r['metadata'].get('category', 'Général') for r in search_results[:2]]
                    
            elif search_results:
                # No LLM, just use vector results
                result["response"] = "\n\n".join(
                    [r['text'] for r in search_results[:2]]
                )
                result["method"] = "vector_only"
                result["confidence"] = search_results[0]['score']
                result["sources"] = [r['metadata'].get('category', 'Général') for r in search_results[:2]]
            else:
                result["error"] = "No search results and LLM generation failed"
                result["method"] = "error"
            
            # 7. Save response to history
            if result["response"]:
                conversation_manager.add_message(
                    session_id,
                    'assistant',
                    result["response"],
                    metadata={
                        'confidence': result["confidence"],
                        'method': result["method"],
                        'sources': result["sources"]
                    }
                )
            
            return result
            
        except Exception as e:
            print(f"❌ RAG Error: {e}")
            result["error"] = str(e)
            result["method"] = "error"
            return result
    
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
