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
from mcp_servers.git_analyzer_client import GitAnalyzerClient
from mcp_servers.weather_remote_client import WeatherRemoteClient
from chatbot.anthropic_client import AnthropicClient
from chatbot.context_manager import ContextManager
from chatbot.intent_detector import IntentDetector
from chatbot.filesystem_executor import FilesystemExecutor
from chatbot.git_executor import GitExecutor
from chatbot.git_analyzer_executor import GitAnalyzerExecutor
from chatbot.weather_executor import WeatherExecutor

class MCPChatbot:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.git_analyzer_client = GitAnalyzerClient()
        self.weather_client = WeatherRemoteClient("https://git-mcp-server-production-a0cf.up.railway.app")
        self.anthropic_client = AnthropicClient()
        self.context_manager = ContextManager()
        self.intent_detector = IntentDetector(self.anthropic_client)
        self.filesystem_executor = FilesystemExecutor(self.mcp_client)
        self.git_executor = GitExecutor(self.mcp_client)
        self.git_analyzer_executor = GitAnalyzerExecutor(self.git_analyzer_client)
        self.weather_executor = WeatherExecutor(self.weather_client)
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
        """Initialize MCP servers"""
        try:
            # Start filesystem server
            fs_success = await self.mcp_client.start_filesystem_server()
            if not fs_success:
                self.logger.error("Failed to start filesystem server")
                return False
            
            # Start Git server
            git_success = await self.mcp_client.start_git_server()
            if not git_success:
                self.logger.error("Failed to start Git server")
                return False
            
            # Start Git Analyzer server
            analyzer_success = await self.git_analyzer_client.start_analyzer_server()
            if not analyzer_success:
                self.logger.error("Failed to start Git Analyzer server")
                return False
            
            # Test Weather server connection
            weather_health = await self.weather_client.health_check()
            if not weather_health["success"]:
                self.logger.error("Failed to connect to Weather server")
                return False
            
            self.logger.info("MCP servers initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP servers: {e}")
            return False
    
    async def process_message(self, user_message: str) -> str:
        """Process user message and return response"""
        try:
            # Add user message to context
            self.context_manager.add_message("user", user_message)
            
            # Get context for AI
            context = self.context_manager.get_context()
            
            # Check if message contains Weather intent using LLM (most specific first)
            weather_intent = await self.intent_detector.detect_weather_intent(user_message)
            
            if weather_intent:
                response = await self.weather_executor.execute_weather_intent(weather_intent, user_message)
                # Add Weather response to context
                self.context_manager.add_message("assistant", response)
                return response
            
            # Check if message contains Git Analyzer intent using LLM
            git_analyzer_intent = await self.intent_detector.detect_git_analyzer_intent(user_message)
            
            if git_analyzer_intent:
                response = await self.git_analyzer_executor.execute_git_analyzer_intent(git_analyzer_intent, user_message)
                # Add Git Analyzer response to context
                self.context_manager.add_message("assistant", response)
                return response
            
            # Check if message contains Git intent using LLM
            git_intent = await self.intent_detector.detect_git_intent(user_message)
            
            if git_intent:
                response = await self.git_executor.execute_git_intent(git_intent, user_message)
                # Add Git response to context
                self.context_manager.add_message("assistant", response)
                return response
            
            # Check if message contains filesystem intent using LLM (least specific last)
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
        print("🌤️ Weather MCP Commands:")
        print("- weather in <city>")
        print("- forecast in <city>")
        print("- weather alerts in <city>")
        print("\n📁 Filesystem MCP Commands:")
        print("- list files / ls")
        print("- read file <path>")
        print("- write file <path> <content>")
        print("\n📚 Git MCP Commands:")
        print("- git status")
        print("- git add <files>")
        print("- git commit <message>")
        print("- git log")
        print("- git init")
        print("- git branch")
        print("\n🔍 Git Analyzer Commands:")
        print("- analyze repository")
        print("- get code metrics <file>")
        print("- detect smells")
        print("- analyze contributors")
        print("- get hotspots")
        print("- generate report <analysis_id>")
        print("\n💬 General Conversation:")
        print("- Type any message for general conversation")
        print("- Type 'quit' to exit\n")
        
        # Initialize MCP servers
        if not await self.initialize():
            print("❌ Failed to initialize MCP servers")
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
            await self.git_analyzer_client.close()
            await self.weather_client.close()
    
