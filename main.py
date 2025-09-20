#!/usr/bin/env python3
"""
Main entry point for the Git MCP Server project
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_chatbot import MCPChatbot

async def main():
    """Main entry point"""
    try:
        # Start the MCP chatbot
        chatbot = MCPChatbot()
        await chatbot.run_interactive()
    except Exception as e:
        print(f"Failed to start chatbot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())