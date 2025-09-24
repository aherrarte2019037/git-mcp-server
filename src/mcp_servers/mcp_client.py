"""
MCP Client using official MCP Python SDK
Connects to filesystem MCP server
"""
import asyncio
import json
import os
import subprocess
from typing import Dict, Any, List, Optional
import logging

class MCPClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.filesystem_process: Optional[subprocess.Popen] = None
        self.git_process: Optional[subprocess.Popen] = None
    
    async def start_filesystem_server(self):
        """Start the filesystem MCP server"""
        try:
            # Start the filesystem server as a subprocess
            self.filesystem_process = subprocess.Popen(
                ["npx", "@modelcontextprotocol/server-filesystem", os.getcwd()],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.logger.info("Filesystem MCP server started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start filesystem server: {e}")
            return False
    
    async def start_git_server(self):
        """Start the Git MCP server"""
        try:
            # Start the Git server as a subprocess using uvx
            self.git_process = subprocess.Popen(
                ["uvx", "mcp-server-git", "--repository", os.getcwd()],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Initialize the MCP connection
            init_result = await self._initialize_mcp_connection("git")
            if not init_result:
                self.logger.error("Failed to initialize Git MCP connection")
                return False
            
            self.logger.info("Git MCP server started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Git server: {e}")
            return False
    
    async def _initialize_mcp_connection(self, server_type: str) -> bool:
        """Initialize MCP connection with the server"""
        try:
            process = self.filesystem_process if server_type == "filesystem" else self.git_process
            server_name = "Filesystem" if server_type == "filesystem" else "Git"
            
            if not process:
                return False
            
            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "mcp-chatbot",
                        "version": "1.0.0"
                    }
                }
            }
            
            # Send request
            request_json = json.dumps(init_request) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            if not response_line:
                return False
            
            response = json.loads(response_line.strip())
            
            if "error" in response:
                self.logger.error(f"Failed to initialize {server_name} MCP: {response['error']}")
                return False
            
            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            
            notification_json = json.dumps(initialized_notification) + "\n"
            process.stdin.write(notification_json)
            process.stdin.flush()
            
            self.logger.info(f"{server_name} MCP connection initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing {server_type} MCP connection: {e}")
            return False
    
    async def _send_mcp_request(self, method: str, params: Dict[str, Any], server_type: str = "filesystem") -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        try:
            process = self.filesystem_process if server_type == "filesystem" else self.git_process
            server_name = "Filesystem" if server_type == "filesystem" else "Git"
            
            if not process:
                return {"success": False, "error": f"{server_name} server not started"}
            
            # Create JSON-RPC request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            # Log the request
            self.logger.info(f"MCP {server_name} JSON-RPC request: {json.dumps(request, indent=2)}")
            
            # Send request
            request_json = json.dumps(request) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            if not response_line:
                return {"success": False, "error": "No response from server"}
            
            response = json.loads(response_line.strip())
            
            # Log the response
            self.logger.info(f"MCP {server_name} JSON-RPC response: {json.dumps(response, indent=2)}")
            
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            return {"success": True, "data": response.get("result", {})}
            
        except Exception as e:
            self.logger.error(f"MCP {server_name} JSON-RPC error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def filesystem_list_files(self, path: str = ".") -> Dict[str, Any]:
        """List files using MCP filesystem server"""
        self.logger.info(f"MCP filesystem operation: list_directory - path: {path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "list_directory",
            "arguments": {"path": path}
        })
        self.logger.info(f"MCP filesystem response: {result}")
        return result
    
    async def filesystem_read_file(self, path: str) -> Dict[str, Any]:
        """Read file using MCP filesystem server"""
        self.logger.info(f"MCP filesystem operation: read_file - path: {path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "read_file",
            "arguments": {"path": path}
        })
        self.logger.info(f"MCP filesystem response: {result}")
        return result
    
    async def filesystem_write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write file using MCP filesystem server"""
        self.logger.info(f"MCP filesystem operation: write_file - path: {path}, content_length: {len(content)}")
        result = await self._send_mcp_request("tools/call", {
            "name": "write_file",
            "arguments": {
                "path": path,
                "content": content
            }
        })
        self.logger.info(f"MCP filesystem response: {result}")
        return result
    
    async def filesystem_create_directory(self, path: str) -> Dict[str, Any]:
        """Create directory using MCP filesystem server"""
        self.logger.info(f"MCP filesystem operation: create_directory - path: {path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "create_directory",
            "arguments": {
                "path": path
            }
        })
        self.logger.info(f"MCP filesystem response: {result}")
        return result
    
    # Git operations
    async def git_status(self, repo_path: str = ".") -> Dict[str, Any]:
        """Get Git status"""
        self.logger.info(f"MCP Git operation: git_status")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_status",
            "arguments": {"repo_path": repo_path}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result
    
    async def git_add(self, repo_path: str, files: List[str]) -> Dict[str, Any]:
        """Add files to Git staging area"""
        self.logger.info(f"MCP Git operation: git_add - files: {files}")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_add",
            "arguments": {"repo_path": repo_path, "files": files}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result
    
    async def git_commit(self, repo_path: str, message: str) -> Dict[str, Any]:
        """Create a Git commit"""
        self.logger.info(f"MCP Git operation: git_commit - message: {message}")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_commit",
            "arguments": {"repo_path": repo_path, "message": message}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result
    
    async def git_log(self, repo_path: str, max_count: int = 10) -> Dict[str, Any]:
        """Get Git log"""
        self.logger.info(f"MCP Git operation: git_log - max_count: {max_count}")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_log",
            "arguments": {"repo_path": repo_path, "max_count": max_count}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result
    
    async def git_init(self, repo_path: str) -> Dict[str, Any]:
        """Initialize a Git repository"""
        self.logger.info(f"MCP Git operation: git_init")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_init",
            "arguments": {"repo_path": repo_path}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result
    
    async def git_branch(self, repo_path: str, branch_type: str = "local") -> Dict[str, Any]:
        """List Git branches"""
        self.logger.info(f"MCP Git operation: git_branch - branch_type: {branch_type}")
        result = await self._send_mcp_request("tools/call", {
            "name": "git_branch",
            "arguments": {"repo_path": repo_path, "branch_type": branch_type}
        }, "git")
        self.logger.info(f"MCP Git response: {result}")
        return result

    async def close(self):
        """Close MCP server connection"""
        try:
            if self.filesystem_process:
                self.filesystem_process.terminate()
                self.filesystem_process.wait()
                self.filesystem_process = None
            
            if self.git_process:
                self.git_process.terminate()
                self.git_process.wait()
                self.git_process = None
            
            self.logger.info("MCP server connection closed")
        except Exception as e:
            self.logger.error(f"Error closing MCP connection: {e}")
