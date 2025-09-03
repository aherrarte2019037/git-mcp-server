"""
Anthropic API client for the chatbot
"""
import anthropic
from typing import List, Dict, Any
from ..config import ANTHROPIC_API_KEY
from ..utils import log_mcp_interaction

class AnthropicClient:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = "claude-3-haiku-20240307"  # Using Haiku for cost efficiency
    
    def send_message(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """
        Send a message to Anthropic API and get response
        
        Args:
            message: User message
            context: Previous conversation context
            
        Returns:
            AI response
        """
        try:
            # Prepare messages for API
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": message})
            
            # Log the request
            log_mcp_interaction("anthropic_request", {
                "message": message,
                "context_length": len(context) if context else 0
            })
            
            # Send to Anthropic
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=messages
            )
            
            ai_response = response.content[0].text
            
            # Log the response
            log_mcp_interaction("anthropic_response", {
                "response": ai_response,
                "usage": response.usage
            })
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error calling Anthropic API: {str(e)}"
            log_mcp_interaction("anthropic_error", {"error": error_msg})
            return f"Sorry, I encountered an error: {error_msg}"
