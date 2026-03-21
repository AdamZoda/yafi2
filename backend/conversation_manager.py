"""
Conversation Manager for YAFI
Handles conversation history and context for multi-turn dialogues
"""

from typing import List, Dict, Optional
from datetime import datetime


class ConversationManager:
    """Manages conversation sessions and history"""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize conversation manager
        
        Args:
            max_history: Maximum number of messages to keep per session
        """
        self.sessions: Dict[str, List[Dict]] = {}
        self.max_history = max_history
        self.session_metadata: Dict[str, Dict] = {}
        self.session_states: Dict[str, Dict] = {} # For interactive quiz state
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to the conversation history
        
        Args:
            session_id: Unique session identifier
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (sources, scores, etc.)
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            self.session_metadata[session_id] = {
                'created_at': datetime.now().isoformat(),
                'message_count': 0
            }
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.sessions[session_id].append(message)
        self.session_metadata[session_id]['message_count'] += 1
        
        # Trim history if too long
        if len(self.sessions[session_id]) > self.max_history * 2:  # *2 because user+assistant
            self.sessions[session_id] = self.sessions[session_id][-self.max_history * 2:]
    
    def get_history(self, session_id: str, last_n: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            last_n: Number of last messages to return (None = all)
            
        Returns:
            List of messages
        """
        if session_id not in self.sessions:
            return []
        
        history = self.sessions[session_id]
        
        if last_n:
            return history[-last_n:]
        
        return history
    
    def get_context_summary(self, session_id: str, max_messages: int = 4) -> str:
        """
        Get a formatted summary of recent conversation
        
        Args:
            session_id: Session identifier
            max_messages: Maximum messages to include
            
        Returns:
            Formatted conversation context
        """
        history = self.get_history(session_id, last_n=max_messages)
        
        if not history:
            return ""
        
        context_lines = []
        for msg in history:
            role = "Utilisateur" if msg['role'] == 'user' else "Assistant"
            content = msg['content'][:150]  # Truncate long messages
            context_lines.append(f"{role}: {content}")
        
        return "\n".join(context_lines)
    
    def get_last_topic(self, session_id: str) -> Optional[str]:
        """
        Extract the last topic discussed from conversation
        
        Args:
            session_id: Session identifier
            
        Returns:
            Last topic or None
        """
        history = self.get_history(session_id, last_n=2)
        
        if not history:
            return None
        
        # Get last user message
        for msg in reversed(history):
            if msg['role'] == 'user':
                return msg['content']
        
        return None
    
    def clear_session(self, session_id: str):
        """Clear a specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_metadata:
            del self.session_metadata[session_id]
        if session_id in self.session_states:
            del self.session_states[session_id]

    def set_state(self, session_id: str, state_name: str, data: Dict = None):
        """Set an active state for the session (e.g. 'QUIZ_Q1')"""
        if session_id not in self.session_states:
            self.session_states[session_id] = {}
        self.session_states[session_id]['current'] = state_name
        self.session_states[session_id]['data'] = data or {}

    def get_state(self, session_id: str) -> Optional[Dict]:
        """Get the current state and its data"""
        return self.session_states.get(session_id)
        
    def update_state_data(self, session_id: str, key: str, value: any):
        """Update data within the current state"""
        if session_id in self.session_states:
            self.session_states[session_id]['data'][key] = value

    def clear_state(self, session_id: str):
        """Clear the active state"""
        if session_id in self.session_states:
            del self.session_states[session_id]
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get metadata about a session"""
        return self.session_metadata.get(session_id)
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        return list(self.sessions.keys())


# Global instance
conversation_manager = ConversationManager(max_history=10)


if __name__ == "__main__":
    # Test the conversation manager
    manager = ConversationManager()
    
    # Simulate a conversation
    session_id = "test_session_123"
    
    manager.add_message(session_id, 'user', "C'est quoi l'ENSA ?")
    manager.add_message(session_id, 'assistant', "L'ENSA est une école d'ingénieurs...")
    manager.add_message(session_id, 'user', "Comment s'y inscrire ?")
    
    # Get history
    history = manager.get_history(session_id)
    print(f"History ({len(history)} messages):")
    for msg in history:
        print(f"  {msg['role']}: {msg['content'][:50]}...")
    
    # Get context summary
    context = manager.get_context_summary(session_id)
    print(f"\nContext Summary:\n{context}")
    
    # Get last topic
    topic = manager.get_last_topic(session_id)
    print(f"\nLast Topic: {topic}")
