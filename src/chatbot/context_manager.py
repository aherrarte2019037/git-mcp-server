"""
Context manager for maintaining conversation history
"""
from typing import List, Dict, Any
from ..utils import log_mcp_interaction

class ContextManager:
    def __init__(self, max_context_length: int = 10):
        self.context: List[Dict[str, str]] = []
        self.max_context_length = max_context_length
    
    def add_interaction(self, user_message: str, ai_response: str):
        """
        Add a user-AI interaction to the context
        
        Args:
            user_message: User's message
            ai_response: AI's response
        """
        # Add user message
        self.context.append({"role": "user", "content": user_message})
        
        # Add AI response
        self.context.append({"role": "assistant", "content": ai_response})
        
        # Trim context if it gets too long
        if len(self.context) > self.max_context_length * 2:  # *2 because we store both user and assistant messages
            self.context = self.context[-self.max_context_length * 2:]
        
        log_mcp_interaction("context_update", {
            "context_length": len(self.context),
            "user_message": user_message[:100] + "..." if len(user_message) > 100 else user_message
        })
    
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
        log_mcp_interaction("context_clear", {})
    
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
