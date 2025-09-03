"""
Filesystem MCP Server Client
"""
import os
import json
from typing import Dict, Any, List
from ..utils import log_mcp_interaction

class FilesystemMCPClient:
    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)
        self.logger = log_mcp_interaction
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a file from the filesystem
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Dictionary with file content and metadata
        """
        try:
            full_path = os.path.join(self.base_path, file_path)
            
            # Security check - ensure path is within base_path
            if not os.path.abspath(full_path).startswith(self.base_path):
                raise ValueError("Access denied: Path outside allowed directory")
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "content": None
                }
            
            if not os.path.isfile(full_path):
                return {
                    "success": False,
                    "error": f"Path is not a file: {file_path}",
                    "content": None
                }
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = {
                "success": True,
                "content": content,
                "file_path": file_path,
                "size": len(content),
                "lines": len(content.splitlines())
            }
            
            self.logger("filesystem_read", {
                "file_path": file_path,
                "size": result["size"],
                "lines": result["lines"]
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "content": None
            }
            
            self.logger("filesystem_read_error", {
                "file_path": file_path,
                "error": str(e)
            })
            
            return error_result
    
    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file
        
        Args:
            file_path: Path to the file to write
            content: Content to write to the file
            
        Returns:
            Dictionary with operation result
        """
        try:
            full_path = os.path.join(self.base_path, file_path)
            
            # Security check
            if not os.path.abspath(full_path).startswith(self.base_path):
                raise ValueError("Access denied: Path outside allowed directory")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result = {
                "success": True,
                "file_path": file_path,
                "size": len(content),
                "lines": len(content.splitlines())
            }
            
            self.logger("filesystem_write", {
                "file_path": file_path,
                "size": result["size"],
                "lines": result["lines"]
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e)
            }
            
            self.logger("filesystem_write_error", {
                "file_path": file_path,
                "error": str(e)
            })
            
            return error_result
    
    def list_directory(self, dir_path: str = ".") -> Dict[str, Any]:
        """
        List contents of a directory
        
        Args:
            dir_path: Path to the directory to list
            
        Returns:
            Dictionary with directory contents
        """
        try:
            full_path = os.path.join(self.base_path, dir_path)
            
            # Security check
            if not os.path.abspath(full_path).startswith(self.base_path):
                raise ValueError("Access denied: Path outside allowed directory")
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"Directory not found: {dir_path}",
                    "contents": []
                }
            
            if not os.path.isdir(full_path):
                return {
                    "success": False,
                    "error": f"Path is not a directory: {dir_path}",
                    "contents": []
                }
            
            contents = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                contents.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            
            result = {
                "success": True,
                "directory_path": dir_path,
                "contents": contents,
                "count": len(contents)
            }
            
            self.logger("filesystem_list", {
                "directory_path": dir_path,
                "count": result["count"]
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "contents": []
            }
            
            self.logger("filesystem_list_error", {
                "directory_path": dir_path,
                "error": str(e)
            })
            
            return error_result
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            Dictionary with operation result
        """
        try:
            full_path = os.path.join(self.base_path, file_path)
            
            # Security check
            if not os.path.abspath(full_path).startswith(self.base_path):
                raise ValueError("Access denied: Path outside allowed directory")
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }
            
            if not os.path.isfile(full_path):
                return {
                    "success": False,
                    "error": f"Path is not a file: {file_path}"
                }
            
            os.remove(full_path)
            
            result = {
                "success": True,
                "file_path": file_path,
                "message": "File deleted successfully"
            }
            
            self.logger("filesystem_delete", {
                "file_path": file_path
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e)
            }
            
            self.logger("filesystem_delete_error", {
                "file_path": file_path,
                "error": str(e)
            })
            
            return error_result
