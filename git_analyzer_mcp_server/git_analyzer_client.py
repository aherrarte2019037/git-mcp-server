"""
Git Analyzer MCP Client
Client for the Git Analyzer MCP Server
"""
import asyncio
import json
import os
import subprocess
from typing import Dict, Any, List, Optional
import logging

class GitAnalyzerClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analyzer_process: Optional[subprocess.Popen] = None
    
    async def start_analyzer_server(self):
        """Start the Git Analyzer MCP server"""
        try:
            # Start the analyzer server as a subprocess
            server_path = os.path.join(os.path.dirname(__file__), "git_analyzer_server.py")
            self.analyzer_process = subprocess.Popen(
                ["python3", server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.logger.info("Git Analyzer MCP server started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Git Analyzer server: {e}")
            return False
    
    async def _send_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        try:
            if not self.analyzer_process:
                return {"success": False, "error": "Git Analyzer server not started"}
            
            # Create JSON-RPC request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            # Log the request
            self.logger.info(f"MCP Git Analyzer JSON-RPC request: {json.dumps(request, indent=2)}")
            
            # Send request
            request_json = json.dumps(request) + "\n"
            self.analyzer_process.stdin.write(request_json)
            self.analyzer_process.stdin.flush()
            
            # Read response
            response_line = self.analyzer_process.stdout.readline()
            if not response_line:
                return {"success": False, "error": "No response from server"}
            
            response = json.loads(response_line.strip())
            
            # Log the response
            self.logger.info(f"MCP Git Analyzer JSON-RPC response: {json.dumps(response, indent=2)}")
            
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            return {"success": True, "data": response.get("result", {})}
            
        except Exception as e:
            self.logger.error(f"MCP Git Analyzer JSON-RPC error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # Git Analyzer operations
    async def analyze_repository(self, repo_path: str = ".", branch: str = "main", depth: int = 100) -> Dict[str, Any]:
        """Complete repository analysis"""
        self.logger.info(f"MCP Git Analyzer operation: analyze_repository - repo_path: {repo_path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "analyze_repository",
            "arguments": {
                "repo_path": repo_path,
                "branch": branch,
                "depth": depth
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def get_code_metrics(self, file_path: str, metric_types: List[str] = None) -> Dict[str, Any]:
        """Get code quality metrics for a specific file"""
        if metric_types is None:
            metric_types = ["lines_of_code", "cyclomatic_complexity", "maintainability_index"]
        
        self.logger.info(f"MCP Git Analyzer operation: get_code_metrics - file_path: {file_path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "get_code_metrics",
            "arguments": {
                "file_path": file_path,
                "metric_types": metric_types
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def detect_smells(self, repo_path: str = ".", sensitivity_level: str = "medium") -> Dict[str, Any]:
        """Detect code smells and antipatterns"""
        self.logger.info(f"MCP Git Analyzer operation: detect_smells - repo_path: {repo_path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "detect_smells",
            "arguments": {
                "repo_path": repo_path,
                "sensitivity_level": sensitivity_level
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def analyze_contributors(self, repo_path: str = ".", time_range: str = "1 year") -> Dict[str, Any]:
        """Analyze contributors and ownership"""
        self.logger.info(f"MCP Git Analyzer operation: analyze_contributors - repo_path: {repo_path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "analyze_contributors",
            "arguments": {
                "repo_path": repo_path,
                "time_range": time_range
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def get_hotspots(self, repo_path: str = ".", threshold: float = 0.8) -> Dict[str, Any]:
        """Identify problematic files (hotspots)"""
        self.logger.info(f"MCP Git Analyzer operation: get_hotspots - repo_path: {repo_path}")
        result = await self._send_mcp_request("tools/call", {
            "name": "get_hotspots",
            "arguments": {
                "repo_path": repo_path,
                "threshold": threshold
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def generate_report(self, analysis_id: str, format: str = "json", sections: List[str] = None) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        if sections is None:
            sections = ["repository_info", "code_metrics", "code_smells", "contributors", "hotspots"]
        
        self.logger.info(f"MCP Git Analyzer operation: generate_report - analysis_id: {analysis_id}")
        result = await self._send_mcp_request("tools/call", {
            "name": "generate_report",
            "arguments": {
                "analysis_id": analysis_id,
                "format": format,
                "sections": sections
            }
        })
        self.logger.info(f"MCP Git Analyzer response: {result}")
        return result
    
    async def close(self):
        """Close MCP server connection"""
        try:
            if self.analyzer_process:
                self.analyzer_process.terminate()
                self.analyzer_process.wait()
                self.analyzer_process = None
            
            self.logger.info("Git Analyzer MCP server connection closed")
        except Exception as e:
            self.logger.error(f"Error closing Git Analyzer MCP connection: {e}")
