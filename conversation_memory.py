"""
Advanced conversation memory management for Role-Based RAG Assistant
Handles context accumulation, summarization, and memory compression
"""
import json
from typing import Dict, List, Any
from datetime import datetime
from database import save_conversation_session, get_conversation_session
from summarize_context import cohere_summarize, document_chunks

class ConversationMemory:
    """Manages conversation memory and context for enhanced multi-turn conversations"""
    
    def __init__(self, user_id: int, session_id: str):
        self.user_id = user_id
        self.session_id = session_id
        self.conversation_buffer = []
        self.context_summary = ""
        self.max_buffer_size = 20  # Maximum number of turns to keep in buffer
        self.compression_threshold = 15  # Compress when buffer exceeds this size
        
        # Load existing session
        self._load_session()
    
    def _load_session(self):
        """Load existing conversation session from database"""
        try:
            self.context_summary = get_conversation_session(self.user_id, self.session_id)
            print(f"Loaded conversation session: {len(self.context_summary)} chars of context")
        except Exception as e:
            print(f"Error loading conversation session: {e}")
            self.context_summary = ""
    
    def add_turn(self, user_message: str, assistant_response: str):
        """Add a conversation turn to memory"""
        turn = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_response
        }
        
        self.conversation_buffer.append(turn)
        
        # Compress memory if needed
        if len(self.conversation_buffer) > self.compression_threshold:
            self._compress_memory()
        
        # Save session
        self._save_session()
    
    def _compress_memory(self):
        """Compress older conversation turns into summary"""
        if len(self.conversation_buffer) <= self.compression_threshold:
            return
        
        print(f"Compressing conversation memory: {len(self.conversation_buffer)} turns")
        
        # Take older turns for compression
        turns_to_compress = self.conversation_buffer[:self.compression_threshold//2]
        self.conversation_buffer = self.conversation_buffer[self.compression_threshold//2:]
        
        # Format turns for summarization
        conversation_text = ""
        for turn in turns_to_compress:
            conversation_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"
        
        # Create document format for Cohere summarization
        documents = document_chunks([{"data": {"text": conversation_text}}])
        
        try:
            # Summarize the conversation segment
            turn_summary = cohere_summarize(documents)
            
            # Combine with existing context summary
            if self.context_summary:
                combined_context = f"{self.context_summary}\n\n--- Recent Conversation ---\n{turn_summary}"
                # Re-summarize if too long
                if len(combined_context) > 2000:
                    combined_docs = document_chunks([{"data": {"text": combined_context}}])
                    self.context_summary = cohere_summarize(combined_docs)
                else:
                    self.context_summary = combined_context
            else:
                self.context_summary = turn_summary
                
            print(f"Memory compressed: {len(self.context_summary)} chars in summary")
            
        except Exception as e:
            print(f"Error compressing memory: {e}")
            # Fallback: keep raw text summary
            if not self.context_summary:
                self.context_summary = conversation_text[:1000] + "..."
    
    def get_conversation_context(self) -> str:
        """Get full conversation context for current query"""
        context_parts = []
        
        # Add compressed context summary
        if self.context_summary:
            context_parts.append(f"=== Conversation History Summary ===\n{self.context_summary}")
        
        # Add recent buffer
        if self.conversation_buffer:
            recent_context = ""
            for turn in self.conversation_buffer[-10:]:  # Last 10 turns
                recent_context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"
            
            if recent_context:
                context_parts.append(f"=== Recent Conversation ===\n{recent_context}")
        
        return "\n\n".join(context_parts)
    
    def enhance_query_with_context(self, current_query: str) -> str:
        """Enhance current query with conversation context"""
        context = self.get_conversation_context()
        
        if not context:
            return current_query
        
        enhanced_query = f"""
{context}

=== Current User Query ===
{current_query}

Please answer the current query considering the full conversation context above. 
Reference previous discussions when relevant and maintain conversation continuity.
"""
        
        return enhanced_query
    
    def _save_session(self):
        """Save current session state to database"""
        try:
            save_conversation_session(self.user_id, self.session_id, self.context_summary)
        except Exception as e:
            print(f"Error saving conversation session: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        return {
            "buffer_size": len(self.conversation_buffer),
            "summary_length": len(self.context_summary),
            "total_context_length": len(self.get_conversation_context()),
            "session_id": self.session_id
        }

# Global memory instances per user session
_memory_instances: Dict[str, ConversationMemory] = {}

def get_conversation_memory(user_id: int, session_id: str = "default") -> ConversationMemory:
    """Get or create conversation memory instance"""
    key = f"{user_id}_{session_id}"
    
    if key not in _memory_instances:
        _memory_instances[key] = ConversationMemory(user_id, session_id)
    
    return _memory_instances[key]

def clear_conversation_memory(user_id: int, session_id: str = "default"):
    """Clear conversation memory for a user session"""
    key = f"{user_id}_{session_id}"
    
    if key in _memory_instances:
        del _memory_instances[key]
    
    # Also clear from database
    try:
        save_conversation_session(user_id, session_id, "")
    except Exception as e:
        print(f"Error clearing conversation session: {e}")
