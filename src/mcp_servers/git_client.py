"""
Git MCP Server Client
"""
import subprocess
import os
from typing import Dict, Any, List
from ..utils import log_mcp_interaction

class GitMCPClient:
    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)
        self.logger = log_mcp_interaction
    
    def _run_git_command(self, command: List[str], cwd: str = None) -> Dict[str, Any]:
        """
        Run a git command and return the result
        
        Args:
            command: Git command as list of strings
            cwd: Working directory for the command
            
        Returns:
            Dictionary with command result
        """
        try:
            if cwd is None:
                cwd = self.base_path
            
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def init_repository(self, repo_path: str = ".") -> Dict[str, Any]:
        """
        Initialize a new git repository
        
        Args:
            repo_path: Path where to initialize the repository
            
        Returns:
            Dictionary with operation result
        """
        try:
            full_path = os.path.join(self.base_path, repo_path)
            os.makedirs(full_path, exist_ok=True)
            
            result = self._run_git_command(["git", "init"], cwd=full_path)
            
            if result["success"]:
                self.logger("git_init", {
                    "repo_path": repo_path,
                    "stdout": result["stdout"]
                })
            else:
                self.logger("git_init_error", {
                    "repo_path": repo_path,
                    "error": result["stderr"]
                })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
            
            self.logger("git_init_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def add_file(self, file_path: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Add a file to git staging area
        
        Args:
            file_path: Path to the file to add
            repo_path: Repository path
            
        Returns:
            Dictionary with operation result
        """
        try:
            full_repo_path = os.path.join(self.base_path, repo_path)
            
            result = self._run_git_command(["git", "add", file_path], cwd=full_repo_path)
            
            if result["success"]:
                self.logger("git_add", {
                    "file_path": file_path,
                    "repo_path": repo_path
                })
            else:
                self.logger("git_add_error", {
                    "file_path": file_path,
                    "repo_path": repo_path,
                    "error": result["stderr"]
                })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
            
            self.logger("git_add_error", {
                "file_path": file_path,
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def commit(self, message: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Create a commit with the given message
        
        Args:
            message: Commit message
            repo_path: Repository path
            
        Returns:
            Dictionary with operation result
        """
        try:
            full_repo_path = os.path.join(self.base_path, repo_path)
            
            result = self._run_git_command(
                ["git", "commit", "-m", message],
                cwd=full_repo_path
            )
            
            if result["success"]:
                self.logger("git_commit", {
                    "message": message,
                    "repo_path": repo_path,
                    "stdout": result["stdout"]
                })
            else:
                self.logger("git_commit_error", {
                    "message": message,
                    "repo_path": repo_path,
                    "error": result["stderr"]
                })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
            
            self.logger("git_commit_error", {
                "message": message,
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def get_status(self, repo_path: str = ".") -> Dict[str, Any]:
        """
        Get git repository status
        
        Args:
            repo_path: Repository path
            
        Returns:
            Dictionary with repository status
        """
        try:
            full_repo_path = os.path.join(self.base_path, repo_path)
            
            result = self._run_git_command(["git", "status", "--porcelain"], cwd=full_repo_path)
            
            if result["success"]:
                # Parse status output
                status_lines = result["stdout"].split('\n') if result["stdout"] else []
                status_info = {
                    "clean": len(status_lines) == 0,
                    "files": []
                }
                
                for line in status_lines:
                    if line.strip():
                        status_info["files"].append({
                            "status": line[:2],
                            "file": line[3:]
                        })
                
                self.logger("git_status", {
                    "repo_path": repo_path,
                    "clean": status_info["clean"],
                    "file_count": len(status_info["files"])
                })
                
                return {
                    "success": True,
                    "status": status_info,
                    "stdout": result["stdout"]
                }
            else:
                return result
                
        except Exception as e:
            error_result = {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
            
            self.logger("git_status_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def get_log(self, repo_path: str = ".", limit: int = 10) -> Dict[str, Any]:
        """
        Get git commit log
        
        Args:
            repo_path: Repository path
            limit: Number of commits to retrieve
            
        Returns:
            Dictionary with commit log
        """
        try:
            full_repo_path = os.path.join(self.base_path, repo_path)
            
            result = self._run_git_command(
                ["git", "log", f"--max-count={limit}", "--oneline"],
                cwd=full_repo_path
            )
            
            if result["success"]:
                commits = []
                for line in result["stdout"].split('\n'):
                    if line.strip():
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            commits.append({
                                "hash": parts[0],
                                "message": parts[1]
                            })
                
                self.logger("git_log", {
                    "repo_path": repo_path,
                    "commit_count": len(commits)
                })
                
                return {
                    "success": True,
                    "commits": commits,
                    "stdout": result["stdout"]
                }
            else:
                return result
                
        except Exception as e:
            error_result = {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
            
            self.logger("git_log_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
