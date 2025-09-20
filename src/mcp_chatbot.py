"""
MCP Chatbot using official MCP servers
Integrates with filesystem and git MCP servers
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_servers.mcp_client import MCPClient
from chatbot.anthropic_client import AnthropicClient
from chatbot.context_manager import ContextManager
from chatbot.intent_detector import IntentDetector
from chatbot.filesystem_executor import FilesystemExecutor

class MCPChatbot:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.anthropic_client = AnthropicClient()
        self.context_manager = ContextManager()
        self.intent_detector = IntentDetector(self.anthropic_client)
        self.filesystem_executor = FilesystemExecutor(self.mcp_client)
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup basic logging"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mcp_interactions.log', mode='w'),
            ]
        )
        return logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize MCP filesystem server"""
        try:
            # Start filesystem server
            fs_success = await self.mcp_client.start_filesystem_server()
            if not fs_success:
                self.logger.error("Failed to start filesystem server")
                return False
            
            self.logger.info("MCP filesystem server initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP server: {e}")
            return False
    
    async def process_message(self, user_message: str) -> str:
        """Process user message and return response"""
        try:
            # Add user message to context
            self.context_manager.add_message("user", user_message)
            
            # Get context for AI
            context = self.context_manager.get_context()
            
            # Check if message contains filesystem intent using LLM
            filesystem_intent = await self.intent_detector.detect_filesystem_intent(user_message)
            
            if filesystem_intent:
                response = await self.filesystem_executor.execute_filesystem_intent(filesystem_intent, user_message)
                # Add filesystem response to context
                self.context_manager.add_message("assistant", response)
                return response
            
            # Send to Anthropic for general conversation
            response = await self.anthropic_client.get_response(user_message, context)
            
            # Add AI response to context
            self.context_manager.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"
    
    
    async def run_interactive(self):
        """Run interactive chatbot session"""
        print("🤖 MCP Filesystem")
        print("Available commands:")
        print("- list files / ls")
        print("- read file <path>")
        print("- write file <path> <content>")
        print("- Type any message for general conversation")
        print("- Type 'quit' to exit\n")
        
        # Initialize MCP filesystem server
        if not await self.initialize():
            print("❌ Failed to initialize MCP filesystem server")
            return
                
        try:
            while True:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Process message
                response = await self.process_message(user_input)
                
                # Display response (only if not empty)
                if response:
                    print(f"Bot: {response}")
                print()  # Empty line for readability
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            # Clean up
            await self.mcp_client.close()
    
