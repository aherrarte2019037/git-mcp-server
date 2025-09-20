"""
Context manager for maintaining conversation history
"""
from typing import List, Dict, Any
import logging

class ContextManager:
    def __init__(self, max_context_length: int = 10):
        self.context: List[Dict[str, str]] = []
        self.max_context_length = max_context_length
    
    def add_message(self, role: str, content: str):
        """
        Add a message to the context
        
        Args:
            role: "user" or "assistant"
            content: Message content
        """
        self.context.append({"role": role, "content": content})
        
        # Trim context if it gets too long
        if len(self.context) > self.max_context_length * 2:  # *2 because we store both user and assistant messages
            self.context = self.context[-self.max_context_length * 2:]
        
        # Log context update
        logging.info(f"Context updated: {len(self.context)} messages")
    
    def add_interaction(self, user_message: str, ai_response: str):
        """
        Add a user-AI interaction to the context
        
        Args:
            user_message: User's message
            ai_response: AI's response
        """
        self.add_message("user", user_message)
        self.add_message("assistant", ai_response)
    
    def get_context(self) -> List[Dict[str, str]]:
        """
        Get the current conversation context
        
        Returns:
            List of conversation messages
        """
        return self.context.copy()
    
    def clear_context(self):
        """Clear the conversation context"""
        self.context = []
        logging.info("Context cleared")
    
    def get_context_summary(self) -> str:
        """
        Get a summary of the current context
        
        Returns:
            String summary of the conversation
        """
        if not self.context:
            return "No previous conversation context."
        
        summary = f"Previous conversation ({len(self.context)//2} exchanges):\n"
        for i in range(0, len(self.context), 2):
            if i + 1 < len(self.context):
                user_msg = self.context[i]["content"][:50] + "..." if len(self.context[i]["content"]) > 50 else self.context[i]["content"]
                summary += f"- User: {user_msg}\n"
        
        return summary
