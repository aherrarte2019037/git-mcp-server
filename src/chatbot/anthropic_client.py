"""
Anthropic API client for the chatbot
"""
import anthropic
from typing import List, Dict, Any
import logging
import os

def log_mcp_interaction(action, data):
    """Simple logging function"""
    logging.info(f"MCP {action}: {data}")

class AnthropicClient:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
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
    
    async def get_response(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """
        Async wrapper for send_message
        """
        return self.send_message(message, context)
