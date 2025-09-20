"""
Main chatbot application
"""
import sys
from .anthropic_client import AnthropicClient
from .context_manager import ContextManager
import logging

class Chatbot:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.context_manager = ContextManager()
        self.logger = logging.getLogger(__name__)
        self.mcp_servers = {}  # Will store MCP server clients
        
    def add_mcp_server(self, name: str, server_client):
        """
        Add an MCP server client to the chatbot
        
        Args:
            name: Name of the MCP server
            server_client: MCP server client instance
        """
        self.mcp_servers[name] = server_client
        self.logger.info(f"MCP server added: {name}")
    
    def process_message(self, user_input: str) -> str:
        """
        Process user message and return AI response
        
        Args:
            user_input: User's input message
            
        Returns:
            AI response
        """
        try:
            # Get current context
            context = self.context_manager.get_context()
            
            # Check if user wants to use MCP servers
            mcp_response = self._check_mcp_usage(user_input)
            if mcp_response:
                # Add MCP interaction to context
                self.context_manager.add_interaction(user_input, mcp_response)
                return mcp_response
            
            # Send to Anthropic API
            ai_response = self.anthropic_client.send_message(user_input, context)
            
            # Add to context
            self.context_manager.add_interaction(user_input, ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.logger.error(error_msg)
            return f"Sorry, I encountered an error: {error_msg}"
    
    def _check_mcp_usage(self, user_input: str) -> str:
        """
        Check if user input requires MCP server usage
        
        Args:
            user_input: User's input message
            
        Returns:
            MCP response if applicable, None otherwise
        """
        user_lower = user_input.lower()
        
        # Check for filesystem operations
        if any(keyword in user_lower for keyword in ['create file', 'read file', 'list files', 'delete file']):
            if 'filesystem' in self.mcp_servers:
                return self._handle_filesystem_request(user_input)
        
        # Check for git operations
        if any(keyword in user_lower for keyword in ['git', 'commit', 'repository', 'repo']):
            if 'git' in self.mcp_servers:
                return self._handle_git_request(user_input)
        
        # Check for git analyzer operations
        if any(keyword in user_lower for keyword in ['analyze', 'stats', 'statistics', 'metrics']):
            if 'git_analyzer' in self.mcp_servers:
                return self._handle_git_analyzer_request(user_input)
        
        return None
    
    def _handle_filesystem_request(self, user_input: str) -> str:
        """Handle filesystem MCP requests"""
        try:
            fs_client = self.mcp_servers.get('filesystem')
            if not fs_client:
                return "Filesystem MCP server not available."
            
            user_lower = user_input.lower()
            
            if 'read file' in user_lower:
                # Extract filename from input
                parts = user_input.split()
                if len(parts) >= 3:
                    filename = parts[2]
                    result = fs_client.read_file(filename)
                    if result["success"]:
                        return f"File content:\n{result['content'][:500]}{'...' if len(result['content']) > 500 else ''}"
                    else:
                        return f"Error reading file: {result['error']}"
                else:
                    return "Please specify a filename to read."
            
            elif 'list files' in user_lower or 'list directory' in user_lower:
                result = fs_client.list_directory()
                if result["success"]:
                    files = [f"{item['name']} ({item['type']})" for item in result["contents"]]
                    return f"Directory contents:\n" + "\n".join(files)
                else:
                    return f"Error listing directory: {result['error']}"
            
            elif 'create file' in user_lower:
                # Simple file creation
                parts = user_input.split()
                if len(parts) >= 3:
                    filename = parts[2]
                    content = " ".join(parts[3:]) if len(parts) > 3 else "Hello, World!"
                    result = fs_client.write_file(filename, content)
                    if result["success"]:
                        return f"File '{filename}' created successfully with {result['lines']} lines."
                    else:
                        return f"Error creating file: {result['error']}"
                else:
                    return "Please specify a filename to create."
            
            else:
                return "Available filesystem operations: read file, list files, create file"
                
        except Exception as e:
            return f"Error with filesystem operation: {str(e)}"
    
    def _handle_git_request(self, user_input: str) -> str:
        """Handle git MCP requests"""
        try:
            git_client = self.mcp_servers.get('git')
            if not git_client:
                return "Git MCP server not available."
            
            user_lower = user_input.lower()
            
            if 'init repository' in user_lower or 'init repo' in user_lower:
                result = git_client.init_repository()
                if result["success"]:
                    return "Git repository initialized successfully."
                else:
                    return f"Error initializing repository: {result['stderr']}"
            
            elif 'add file' in user_lower:
                parts = user_input.split()
                if len(parts) >= 3:
                    filename = parts[2]
                    result = git_client.add_file(filename)
                    if result["success"]:
                        return f"File '{filename}' added to staging area."
                    else:
                        return f"Error adding file: {result['stderr']}"
                else:
                    return "Please specify a filename to add."
            
            elif 'commit' in user_lower:
                parts = user_input.split('"')
                if len(parts) >= 2:
                    message = parts[1]
                    result = git_client.commit(message)
                    if result["success"]:
                        return f"Commit created successfully: {message}"
                    else:
                        return f"Error creating commit: {result['stderr']}"
                else:
                    return "Please provide a commit message in quotes."
            
            elif 'git status' in user_lower:
                result = git_client.get_status()
                if result["success"]:
                    status = result["status"]
                    if status["clean"]:
                        return "Repository is clean - no changes to commit."
                    else:
                        files = [f"{f['file']} ({f['status']})" for f in status["files"]]
                        return f"Repository status:\n" + "\n".join(files)
                else:
                    return f"Error getting status: {result['stderr']}"
            
            else:
                return "Available git operations: init repository, add file, commit, git status"
                
        except Exception as e:
            return f"Error with git operation: {str(e)}"
    
    def _handle_git_analyzer_request(self, user_input: str) -> str:
        """Handle git analyzer MCP requests"""
        try:
            analyzer = self.mcp_servers.get('git_analyzer')
            if not analyzer:
                return "Git Analyzer MCP server not available."
            
            user_lower = user_input.lower()
            
            if 'analyze repository' in user_lower or 'repo info' in user_lower:
                result = analyzer.get_repo_info()
                if result["success"]:
                    stats = result["data"]["statistics"]
                    return f"""Repository Analysis:
- Total Commits: {stats.get('total_commits', 'Unknown')}
- Total Files: {stats.get('total_files', 'Unknown')}
- Lines of Code: {stats.get('lines_of_code', 'Unknown')}
- Repository Size: {stats.get('repository_size', 'Unknown')}
- Current Branch: {stats.get('current_branch', 'Unknown')}
- Last Commit: {stats.get('last_commit', {}).get('message', 'Unknown')}"""
                else:
                    return f"Error analyzing repository: {result['error']}"
            
            elif 'commit stats' in user_lower or 'commit statistics' in user_lower:
                result = analyzer.get_commit_stats()
                if result["success"]:
                    stats = result["data"]["statistics"]
                    return f"""Commit Statistics (Last 30 Days):
- Total Commits: {stats.get('total_commits', 0)}
- Commits per Day: {stats.get('commits_per_day', 0)}
- Top Contributors: {', '.join([f'{author} ({count})' for author, count in stats.get('top_contributors', [])[:3]])}"""
                else:
                    return f"Error getting commit statistics: {result['error']}"
            
            elif 'file stats' in user_lower or 'file statistics' in user_lower:
                result = analyzer.get_file_stats()
                if result["success"]:
                    stats = result["data"]["statistics"]
                    return f"""File Statistics:
- Total Files: {stats.get('total_files', 0)}
- Total Size: {stats.get('total_size_mb', 0)} MB
- Top Extensions: {', '.join([f'{ext} ({count})' for ext, count in list(stats.get('file_extensions', {}).items())[:3]])}"""
                else:
                    return f"Error getting file statistics: {result['error']}"
            
            elif 'generate report' in user_lower:
                result = analyzer.generate_report(format="text")
                if result["success"]:
                    return f"Repository Report Generated:\n{result['data'][:800]}{'...' if len(result['data']) > 800 else ''}"
                else:
                    return f"Error generating report: {result['error']}"
            
            else:
                return "Available git analyzer operations: analyze repository, commit stats, file stats, generate report"
                
        except Exception as e:
            return f"Error with git analyzer operation: {str(e)}"
    
    def run_interactive(self):
        """Run the chatbot in interactive mode"""
        print("- Git MCP Chatbot - Type 'quit' to exit, 'clear' to clear context")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    self.context_manager.clear_context()
                    print("🧹 Context cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Process and display bot response with background
                response = self.process_message(user_input)
                print(f"\n🤖 Bot: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main entry point"""
    try:
        chatbot = Chatbot()
        
        # Initialize MCP servers
        from .init_mcp_servers import initialize_mcp_servers
        initialize_mcp_servers(chatbot)
        
        chatbot.run_interactive()
    except Exception as e:
        print(f"Failed to start chatbot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
