"""
Git Analyzer MCP Server - Simple repository analysis
"""
import os
import subprocess
import json
from datetime import datetime
from typing import Dict, Any, List
import logging

def log_mcp_interaction(action, data):
    """Simple logging function"""
    logging.info(f"MCP {action}: {data}")

class GitAnalyzerMCPServer:
    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)
        self.logger = log_mcp_interaction
    
    def _run_git_command(self, command: List[str], cwd: str = None) -> Dict[str, Any]:
        """Run a git command and return the result"""
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
            
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def get_repo_info(self, repo_path: str = ".") -> Dict[str, Any]:
        """
        Get basic repository information
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Dictionary with repository information
        """
        try:
            full_path = os.path.join(self.base_path, repo_path)
            
            # Check if it's a git repository
            if not os.path.exists(os.path.join(full_path, '.git')):
                return {
                    "success": False,
                    "error": "Not a git repository",
                    "data": None
                }
            
            # Get repository statistics
            stats = {}
            
            # Count commits
            commit_result = self._run_git_command(["git", "rev-list", "--count", "HEAD"], cwd=full_path)
            if commit_result["success"]:
                stats["total_commits"] = int(commit_result["stdout"])
            
            # Count files
            file_result = self._run_git_command(["git", "ls-files"], cwd=full_path)
            if file_result["success"]:
                files = file_result["stdout"].split('\n')
                stats["total_files"] = len([f for f in files if f.strip()])
            
            # Count lines of code (approximate)
            loc_result = self._run_git_command(["git", "ls-files", "|", "xargs", "wc", "-l"], cwd=full_path)
            if loc_result["success"]:
                try:
                    stats["lines_of_code"] = int(loc_result["stdout"].split()[-1])
                except:
                    stats["lines_of_code"] = "Unknown"
            
            # Get repository size
            size_result = self._run_git_command(["du", "-sh", "."], cwd=full_path)
            if size_result["success"]:
                stats["repository_size"] = size_result["stdout"].split()[0]
            
            # Get current branch
            branch_result = self._run_git_command(["git", "branch", "--show-current"], cwd=full_path)
            if branch_result["success"]:
                stats["current_branch"] = branch_result["stdout"]
            
            # Get last commit info
            last_commit_result = self._run_git_command([
                "git", "log", "-1", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=short"
            ], cwd=full_path)
            if last_commit_result["success"]:
                parts = last_commit_result["stdout"].split('|')
                if len(parts) >= 5:
                    stats["last_commit"] = {
                        "hash": parts[0][:8],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    }
            
            result = {
                "success": True,
                "data": {
                    "repository_path": repo_path,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "statistics": stats
                }
            }
            
            self.logger("git_analyzer_repo_info", {
                "repo_path": repo_path,
                "commits": stats.get("total_commits", 0),
                "files": stats.get("total_files", 0)
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "data": None
            }
            
            self.logger("git_analyzer_repo_info_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def get_commit_stats(self, repo_path: str = ".", days: int = 30) -> Dict[str, Any]:
        """
        Get commit statistics for the repository
        
        Args:
            repo_path: Path to the repository
            days: Number of days to analyze
            
        Returns:
            Dictionary with commit statistics
        """
        try:
            full_path = os.path.join(self.base_path, repo_path)
            
            # Get commits in the last N days
            since_date = f"{days} days ago"
            commit_result = self._run_git_command([
                "git", "log", f"--since={since_date}", "--pretty=format:%H|%an|%ad", "--date=short"
            ], cwd=full_path)
            
            if not commit_result["success"]:
                return {
                    "success": False,
                    "error": "Failed to get commit history",
                    "data": None
                }
            
            commits = []
            authors = {}
            
            for line in commit_result["stdout"].split('\n'):
                if line.strip():
                    parts = line.split('|')
                    if len(parts) >= 3:
                        commit_info = {
                            "hash": parts[0][:8],
                            "author": parts[1],
                            "date": parts[2]
                        }
                        commits.append(commit_info)
                        
                        # Count commits per author
                        if parts[1] in authors:
                            authors[parts[1]] += 1
                        else:
                            authors[parts[1]] = 1
            
            # Calculate statistics
            stats = {
                "total_commits": len(commits),
                "period_days": days,
                "commits_per_day": round(len(commits) / days, 2) if days > 0 else 0,
                "top_contributors": sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5],
                "recent_commits": commits[:10]  # Last 10 commits
            }
            
            result = {
                "success": True,
                "data": {
                    "repository_path": repo_path,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "statistics": stats
                }
            }
            
            self.logger("git_analyzer_commit_stats", {
                "repo_path": repo_path,
                "total_commits": stats["total_commits"],
                "contributors": len(authors)
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "data": None
            }
            
            self.logger("git_analyzer_commit_stats_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def get_file_stats(self, repo_path: str = ".") -> Dict[str, Any]:
        """
        Get file statistics for the repository
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Dictionary with file statistics
        """
        try:
            full_path = os.path.join(self.base_path, repo_path)
            
            # Get all files in the repository
            file_result = self._run_git_command(["git", "ls-files"], cwd=full_path)
            
            if not file_result["success"]:
                return {
                    "success": False,
                    "error": "Failed to get file list",
                    "data": None
                }
            
            files = [f.strip() for f in file_result["stdout"].split('\n') if f.strip()]
            
            # Analyze file extensions
            extensions = {}
            total_size = 0
            
            for file_path in files:
                full_file_path = os.path.join(full_path, file_path)
                if os.path.exists(full_file_path):
                    # Get file extension
                    ext = os.path.splitext(file_path)[1].lower()
                    if not ext:
                        ext = "no_extension"
                    
                    if ext in extensions:
                        extensions[ext] += 1
                    else:
                        extensions[ext] = 1
                    
                    # Get file size
                    try:
                        total_size += os.path.getsize(full_file_path)
                    except:
                        pass
            
            # Get largest files
            largest_files = []
            for file_path in files[:20]:  # Check first 20 files for size
                full_file_path = os.path.join(full_path, file_path)
                if os.path.exists(full_file_path):
                    try:
                        size = os.path.getsize(full_file_path)
                        largest_files.append({
                            "file": file_path,
                            "size": size,
                            "size_mb": round(size / (1024 * 1024), 2)
                        })
                    except:
                        pass
            
            largest_files.sort(key=lambda x: x["size"], reverse=True)
            
            stats = {
                "total_files": len(files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_extensions": dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True)),
                "largest_files": largest_files[:10]
            }
            
            result = {
                "success": True,
                "data": {
                    "repository_path": repo_path,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "statistics": stats
                }
            }
            
            self.logger("git_analyzer_file_stats", {
                "repo_path": repo_path,
                "total_files": stats["total_files"],
                "total_size_mb": stats["total_size_mb"]
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "data": None
            }
            
            self.logger("git_analyzer_file_stats_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def generate_report(self, repo_path: str = ".", format: str = "json") -> Dict[str, Any]:
        """
        Generate a comprehensive repository analysis report
        
        Args:
            repo_path: Path to the repository
            format: Report format (json, text)
            
        Returns:
            Dictionary with the generated report
        """
        try:
            # Get all statistics
            repo_info = self.get_repo_info(repo_path)
            commit_stats = self.get_commit_stats(repo_path)
            file_stats = self.get_file_stats(repo_path)
            
            if not all([repo_info["success"], commit_stats["success"], file_stats["success"]]):
                return {
                    "success": False,
                    "error": "Failed to gather repository statistics",
                    "data": None
                }
            
            # Combine all data
            report_data = {
                "repository_analysis": {
                    "repository_path": repo_path,
                    "generated_at": datetime.now().isoformat(),
                    "repository_info": repo_info["data"],
                    "commit_statistics": commit_stats["data"],
                    "file_statistics": file_stats["data"]
                }
            }
            
            # Format the report
            if format.lower() == "text":
                report_text = self._format_text_report(report_data)
                result = {
                    "success": True,
                    "format": "text",
                    "data": report_text
                }
            else:  # Default to JSON
                result = {
                    "success": True,
                    "format": "json",
                    "data": report_data
                }
            
            self.logger("git_analyzer_report", {
                "repo_path": repo_path,
                "format": format
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "data": None
            }
            
            self.logger("git_analyzer_report_error", {
                "repo_path": repo_path,
                "error": str(e)
            })
            
            return error_result
    
    def _format_text_report(self, data: Dict[str, Any]) -> str:
        """Format the report as text"""
        repo_data = data["repository_analysis"]
        repo_info = repo_data["repository_info"]["statistics"]
        commit_stats = repo_data["commit_statistics"]["statistics"]
        file_stats = repo_data["file_statistics"]["statistics"]
        
        report = f"""
# Git Repository Analysis Report

**Repository:** {repo_data["repository_path"]}
**Generated:** {repo_data["generated_at"]}

## Repository Overview
- **Total Commits:** {repo_info.get("total_commits", "Unknown")}
- **Total Files:** {repo_info.get("total_files", "Unknown")}
- **Lines of Code:** {repo_info.get("lines_of_code", "Unknown")}
- **Repository Size:** {repo_info.get("repository_size", "Unknown")}
- **Current Branch:** {repo_info.get("current_branch", "Unknown")}

## Recent Activity (Last 30 Days)
- **Commits:** {commit_stats.get("total_commits", 0)}
- **Commits per Day:** {commit_stats.get("commits_per_day", 0)}
- **Top Contributors:**
"""
        
        for author, count in commit_stats.get("top_contributors", []):
            report += f"  - {author}: {count} commits\n"
        
        report += f"""
## File Statistics
- **Total Files:** {file_stats.get("total_files", 0)}
- **Total Size:** {file_stats.get("total_size_mb", 0)} MB
- **File Extensions:**
"""
        
        for ext, count in list(file_stats.get("file_extensions", {}).items())[:5]:
            report += f"  - {ext}: {count} files\n"
        
        report += "\n## Largest Files\n"
        for file_info in file_stats.get("largest_files", [])[:5]:
            report += f"  - {file_info['file']}: {file_info['size_mb']} MB\n"
        
        return report
