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
    
    
    async def _send_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        try:
            if not self.filesystem_process:
                return {"success": False, "error": "Filesystem server not started"}
            
            # Create JSON-RPC request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            # Log the request
            self.logger.info(f"MCP JSON-RPC request: {json.dumps(request, indent=2)}")
            
            # Send request
            request_json = json.dumps(request) + "\n"
            self.filesystem_process.stdin.write(request_json)
            self.filesystem_process.stdin.flush()
            
            # Read response
            response_line = self.filesystem_process.stdout.readline()
            if not response_line:
                return {"success": False, "error": "No response from server"}
            
            response = json.loads(response_line.strip())
            
            # Log the response
            self.logger.info(f"MCP JSON-RPC response: {json.dumps(response, indent=2)}")
            
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            return {"success": True, "data": response.get("result", {})}
            
        except Exception as e:
            self.logger.error(f"MCP JSON-RPC error: {str(e)}")
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
    
    async def close(self):
        """Close MCP server connection"""
        try:
            if self.filesystem_process:
                self.filesystem_process.terminate()
                self.filesystem_process.wait()
                self.filesystem_process = None
            
            self.logger.info("MCP server connection closed")
        except Exception as e:
            self.logger.error(f"Error closing MCP connection: {e}")
