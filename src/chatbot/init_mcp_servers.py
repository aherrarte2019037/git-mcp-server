"""
Initialize MCP servers for the chatbot
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mcp_servers.filesystem_client import FilesystemMCPClient
from mcp_servers.git_client import GitMCPClient
from mcp_servers.git_analyzer_server import GitAnalyzerMCPServer

def initialize_mcp_servers(chatbot):
    """
    Initialize all MCP servers and add them to the chatbot
    
    Args:
        chatbot: Chatbot instance to add servers to
    """
    try:
        # Initialize Filesystem MCP Client
        fs_client = FilesystemMCPClient()
        chatbot.add_mcp_server('filesystem', fs_client)
        print("✅ Filesystem MCP server initialized")
        
        # Initialize Git MCP Client
        git_client = GitMCPClient()
        chatbot.add_mcp_server('git', git_client)
        print("✅ Git MCP server initialized")
        
        # Initialize Git Analyzer MCP Server
        git_analyzer = GitAnalyzerMCPServer()
        chatbot.add_mcp_server('git_analyzer', git_analyzer)
        print("✅ Git Analyzer MCP server initialized")
        
        print("\nAvailable operations:")
        print("- Filesystem: read file, list files, create file")
        print("- Git: init repository, add file, commit, git status")
        print("- Git Analyzer: analyze repository, commit stats, file stats, generate report")
        
    except Exception as e:
        print(f"❌ Error initializing MCP servers: {str(e)}")
        raise
