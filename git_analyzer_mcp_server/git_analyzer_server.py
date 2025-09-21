#!/usr/bin/env python3
"""
Git Analyzer MCP Server
Advanced Git repository analysis with code quality metrics, smell detection, and contributor analysis
"""
import asyncio
import json
import sys
import os
import subprocess
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CodeMetrics:
    """Code quality metrics"""
    lines_of_code: int
    cyclomatic_complexity: int
    maintainability_index: float
    technical_debt: float
    code_coverage: float

@dataclass
class CodeSmell:
    """Code smell detection result"""
    type: str
    severity: str
    file_path: str
    line_number: int
    description: str
    suggestion: str

@dataclass
class Contributor:
    """Contributor analysis"""
    name: str
    email: str
    commits: int
    lines_added: int
    lines_removed: int
    ownership_percentage: float
    first_commit: datetime
    last_commit: datetime

class GitAnalyzerServer:
    """Git Analyzer MCP Server implementation"""
    
    def __init__(self):
        self.repo_path = "."
        self.analysis_cache = {}
        
    async def analyze_repository(self, repo_path: str, branch: str = "main", depth: int = 100) -> Dict[str, Any]:
        """Complete repository analysis"""
        try:
            logger.info(f"Starting repository analysis: {repo_path}, branch: {branch}, depth: {depth}")
            
            # Change to repository directory
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            try:
                # Get repository information
                repo_info = await self._get_repo_info()
                
                # Analyze code metrics
                code_metrics = await self._analyze_code_metrics(repo_path)
                
                # Detect code smells
                code_smells = await self._detect_code_smells(repo_path, "medium")
                
                # Analyze contributors
                contributors = await self._analyze_contributors(repo_path, "1 year")
                
                # Get hotspots
                hotspots = await self._get_hotspots(repo_path, 0.8)
                
                analysis_result = {
                    "repository_info": repo_info,
                    "code_metrics": code_metrics,
                    "code_smells": code_smells,
                    "contributors": contributors,
                    "hotspots": hotspots,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "branch": branch,
                    "depth": depth
                }
                
                # Cache the analysis
                analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.analysis_cache[analysis_id] = analysis_result
                
                return {
                    "success": True,
                    "analysis_id": analysis_id,
                    "data": analysis_result
                }
                
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"Error analyzing repository: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_code_metrics(self, file_path: str, metric_types: List[str] = None) -> Dict[str, Any]:
        """Get code quality metrics for a specific file"""
        try:
            if metric_types is None or len(metric_types) == 0:
                metric_types = ["lines_of_code", "cyclomatic_complexity", "maintainability_index"]
            
            logger.info(f"Analyzing code metrics for: {file_path}, metric_types: {metric_types}")
            
            metrics = {}
            
            if "lines_of_code" in metric_types:
                metrics["lines_of_code"] = await self._count_lines_of_code(file_path)
            
            if "cyclomatic_complexity" in metric_types:
                metrics["cyclomatic_complexity"] = await self._calculate_cyclomatic_complexity(file_path)
            
            if "maintainability_index" in metric_types:
                metrics["maintainability_index"] = await self._calculate_maintainability_index(file_path)
            
            if "technical_debt" in metric_types:
                metrics["technical_debt"] = await self._calculate_technical_debt(file_path)
            
            if "code_coverage" in metric_types:
                metrics["code_coverage"] = await self._calculate_code_coverage(file_path)
            
            return {"success": True, "data": metrics}
            
        except Exception as e:
            logger.error(f"Error getting code metrics: {e}")
            return {"success": False, "error": str(e)}
    
    async def detect_smells(self, repo_path: str, sensitivity_level: str = "medium") -> Dict[str, Any]:
        """Detect code smells and antipatterns"""
        try:
            logger.info(f"Detecting code smells in: {repo_path}, sensitivity: {sensitivity_level}")
            
            smells = []
            
            # Find Python files
            python_files = await self._find_python_files(repo_path)
            
            for file_path in python_files:
                file_smells = await self._analyze_file_smells(file_path, sensitivity_level)
                smells.extend(file_smells)
            
            # Categorize smells by type
            smell_categories = {}
            for smell in smells:
                smell_type = smell["type"]
                if smell_type not in smell_categories:
                    smell_categories[smell_type] = []
                smell_categories[smell_type].append(smell)
            
            return {
                "success": True,
                "data": {
                    "total_smells": len(smells),
                    "smells_by_type": smell_categories,
                    "sensitivity_level": sensitivity_level,
                    "files_analyzed": len(python_files)
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting smells: {e}")
            return {"success": False, "error": str(e)}
    
    async def analyze_contributors(self, repo_path: str, time_range: str = "1 year") -> Dict[str, Any]:
        """Analyze contributors and ownership"""
        try:
            logger.info(f"Analyzing contributors in: {repo_path}, time_range: {time_range}")
            
            # Get git log with author information
            cmd = ["git", "log", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=iso"]
            
            # Add time range filter
            if time_range == "1 year":
                cmd.extend(["--since=1 year ago"])
            elif time_range == "6 months":
                cmd.extend(["--since=6 months ago"])
            elif time_range == "1 month":
                cmd.extend(["--since=1 month ago"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to get git log"}
            
            # Parse contributors
            contributors = {}
            total_commits = 0
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                parts = line.split('|', 4)
                if len(parts) < 5:
                    continue
                
                commit_hash, name, email, date_str, message = parts
                
                if email not in contributors:
                    contributors[email] = {
                        "name": name,
                        "email": email,
                        "commits": 0,
                        "lines_added": 0,
                        "lines_removed": 0,
                        "first_commit": date_str,
                        "last_commit": date_str
                    }
                
                contributors[email]["commits"] += 1
                contributors[email]["last_commit"] = date_str
                total_commits += 1
                
                # Get lines changed for this commit
                lines_changed = await self._get_commit_lines_changed(repo_path, commit_hash)
                contributors[email]["lines_added"] += lines_changed["added"]
                contributors[email]["lines_removed"] += lines_changed["removed"]
            
            # Calculate ownership percentages
            for email, contributor in contributors.items():
                contributor["ownership_percentage"] = (contributor["commits"] / total_commits) * 100
            
            # Sort by commits
            sorted_contributors = sorted(contributors.values(), key=lambda x: x["commits"], reverse=True)
            
            return {
                "success": True,
                "data": {
                    "total_contributors": len(contributors),
                    "total_commits": total_commits,
                    "contributors": sorted_contributors,
                    "time_range": time_range
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing contributors: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_hotspots(self, repo_path: str, threshold: float = 0.8) -> Dict[str, Any]:
        """Identify problematic files (hotspots)"""
        try:
            logger.info(f"Identifying hotspots in: {repo_path}, threshold: {threshold}")
            
            # Get file change frequency
            cmd = ["git", "log", "--name-only", "--pretty=format:", "--since=6 months ago"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to get file change history"}
            
            # Count file changes
            file_changes = {}
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith(' '):
                    file_path = line.strip()
                    if file_path:
                        file_changes[file_path] = file_changes.get(file_path, 0) + 1
            
            # Calculate hotspots based on change frequency
            total_changes = sum(file_changes.values())
            hotspots = []
            
            for file_path, changes in file_changes.items():
                change_frequency = changes / total_changes
                if change_frequency >= threshold:
                    # Get additional metrics for this file
                    file_metrics = await self._get_file_metrics(repo_path, file_path)
                    
                    hotspots.append({
                        "file_path": file_path,
                        "change_frequency": change_frequency,
                        "total_changes": changes,
                        "metrics": file_metrics
                    })
            
            # Sort by change frequency
            hotspots.sort(key=lambda x: x["change_frequency"], reverse=True)
            
            return {
                "success": True,
                "data": {
                    "hotspots": hotspots,
                    "threshold": threshold,
                    "total_files_analyzed": len(file_changes)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting hotspots: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_report(self, analysis_id: str, format: str = "json", sections: List[str] = None) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        try:
            if analysis_id not in self.analysis_cache:
                return {"success": False, "error": "Analysis ID not found"}
            
            analysis_data = self.analysis_cache[analysis_id]
            
            if sections is None:
                sections = ["repository_info", "code_metrics", "code_smells", "contributors", "hotspots"]
            
            report = {
                "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "analysis_id": analysis_id,
                "format": format,
                "sections": sections,
                "generated_at": datetime.now().isoformat()
            }
            
            # Add requested sections
            for section in sections:
                if section in analysis_data:
                    report[section] = analysis_data[section]
            
            # Add summary
            report["summary"] = await self._generate_summary(analysis_data)
            
            return {"success": True, "data": report}
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {"success": False, "error": str(e)}
    
    # Helper methods
    async def _get_repo_info(self) -> Dict[str, Any]:
        """Get basic repository information"""
        try:
            # Get current branch
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
            current_branch = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # Get total commits
            result = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True)
            total_commits = int(result.stdout.strip()) if result.returncode == 0 else 0
            
            # Get repository size
            result = subprocess.run(["du", "-sh", "."], capture_output=True, text=True)
            repo_size = result.stdout.split()[0] if result.returncode == 0 else "unknown"
            
            return {
                "current_branch": current_branch,
                "total_commits": total_commits,
                "repository_size": repo_size,
                "last_commit": await self._get_last_commit_date()
            }
        except Exception as e:
            logger.error(f"Error getting repo info: {e}")
            return {}
    
    async def _detect_code_smells(self, repo_path: str, sensitivity_level: str = "medium") -> Dict[str, Any]:
        """Detect code smells for repository analysis"""
        try:
            smells = []
            
            # Find Python files
            python_files = await self._find_python_files(repo_path)
            
            for file_path in python_files:
                file_smells = await self._analyze_file_smells(file_path, sensitivity_level)
                smells.extend(file_smells)
            
            # Categorize smells by type
            smell_categories = {}
            for smell in smells:
                smell_type = smell["type"]
                if smell_type not in smell_categories:
                    smell_categories[smell_type] = []
                smell_categories[smell_type].append(smell)
            
            return {
                "total_smells": len(smells),
                "smells_by_type": smell_categories,
                "sensitivity_level": sensitivity_level,
                "files_analyzed": len(python_files)
            }
        except Exception as e:
            logger.error(f"Error detecting code smells: {e}")
            return {"total_smells": 0, "smells_by_type": {}, "sensitivity_level": sensitivity_level, "files_analyzed": 0}
    
    async def _analyze_contributors(self, repo_path: str, time_range: str = "1 year") -> Dict[str, Any]:
        """Analyze contributors for repository analysis"""
        try:
            # Get git log with author information
            cmd = ["git", "log", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=iso"]
            
            # Add time range filter
            if time_range == "1 year":
                cmd.extend(["--since=1 year ago"])
            elif time_range == "6 months":
                cmd.extend(["--since=6 months ago"])
            elif time_range == "1 month":
                cmd.extend(["--since=1 month ago"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                return {"total_contributors": 0, "total_commits": 0, "contributors": [], "time_range": time_range}
            
            # Parse contributors
            contributors = {}
            total_commits = 0
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                parts = line.split('|', 4)
                if len(parts) < 5:
                    continue
                
                commit_hash, name, email, date_str, message = parts
                
                if email not in contributors:
                    contributors[email] = {
                        "name": name,
                        "email": email,
                        "commits": 0,
                        "lines_added": 0,
                        "lines_removed": 0,
                        "first_commit": date_str,
                        "last_commit": date_str
                    }
                
                contributors[email]["commits"] += 1
                contributors[email]["last_commit"] = date_str
                total_commits += 1
                
                # Get lines changed for this commit
                lines_changed = await self._get_commit_lines_changed(repo_path, commit_hash)
                contributors[email]["lines_added"] += lines_changed["added"]
                contributors[email]["lines_removed"] += lines_changed["removed"]
            
            # Calculate ownership percentages
            for email, contributor in contributors.items():
                contributor["ownership_percentage"] = (contributor["commits"] / total_commits) * 100 if total_commits > 0 else 0
            
            # Sort by commits
            sorted_contributors = sorted(contributors.values(), key=lambda x: x["commits"], reverse=True)
            
            return {
                "total_contributors": len(contributors),
                "total_commits": total_commits,
                "contributors": sorted_contributors,
                "time_range": time_range
            }
        except Exception as e:
            logger.error(f"Error analyzing contributors: {e}")
            return {"total_contributors": 0, "total_commits": 0, "contributors": [], "time_range": time_range}
    
    async def _get_hotspots(self, repo_path: str, threshold: float = 0.8) -> Dict[str, Any]:
        """Get hotspots for repository analysis"""
        try:
            # Get file change frequency
            cmd = ["git", "log", "--name-only", "--pretty=format:", "--since=6 months ago"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                return {"hotspots": [], "threshold": threshold, "total_files_analyzed": 0}
            
            # Count file changes
            file_changes = {}
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith(' '):
                    file_path = line.strip()
                    if file_path:
                        file_changes[file_path] = file_changes.get(file_path, 0) + 1
            
            # Calculate hotspots based on change frequency
            total_changes = sum(file_changes.values())
            hotspots = []
            
            for file_path, changes in file_changes.items():
                change_frequency = changes / total_changes if total_changes > 0 else 0
                if change_frequency >= threshold:
                    # Get additional metrics for this file
                    file_metrics = await self._get_file_metrics(repo_path, file_path)
                    
                    hotspots.append({
                        "file_path": file_path,
                        "change_frequency": change_frequency,
                        "total_changes": changes,
                        "metrics": file_metrics
                    })
            
            # Sort by change frequency
            hotspots.sort(key=lambda x: x["change_frequency"], reverse=True)
            
            return {
                "hotspots": hotspots,
                "threshold": threshold,
                "total_files_analyzed": len(file_changes)
            }
        except Exception as e:
            logger.error(f"Error getting hotspots: {e}")
            return {"hotspots": [], "threshold": threshold, "total_files_analyzed": 0}
    
    async def _analyze_code_metrics(self, repo_path: str) -> Dict[str, Any]:
        """Analyze code metrics for the repository"""
        python_files = await self._find_python_files(repo_path)
        
        total_lines = 0
        total_complexity = 0
        files_analyzed = 0
        
        for file_path in python_files:
            try:
                lines = await self._count_lines_of_code(file_path)
                complexity = await self._calculate_cyclomatic_complexity(file_path)
                
                total_lines += lines
                total_complexity += complexity
                files_analyzed += 1
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
        
        return {
            "total_files": files_analyzed,
            "total_lines_of_code": total_lines,
            "average_complexity": total_complexity / files_analyzed if files_analyzed > 0 else 0,
            "lines_per_file": total_lines / files_analyzed if files_analyzed > 0 else 0
        }
    
    async def _count_lines_of_code(self, file_path: str) -> int:
        """Count lines of code in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out empty lines and comments
            code_lines = 0
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    code_lines += 1
            
            return code_lines
        except Exception:
            return 0
    
    async def _calculate_cyclomatic_complexity(self, file_path: str) -> int:
        """Calculate cyclomatic complexity for a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple cyclomatic complexity calculation
            complexity = 1  # Base complexity
            
            # Count control flow statements
            complexity += len(re.findall(r'\b(if|elif|while|for|except|with|and|or)\b', content))
            complexity += len(re.findall(r'\b(if|elif|while|for|except|with)\s+.*:', content))
            
            return complexity
        except Exception:
            return 1
    
    async def _calculate_maintainability_index(self, file_path: str) -> float:
        """Calculate maintainability index (simplified)"""
        try:
            lines = await self._count_lines_of_code(file_path)
            complexity = await self._calculate_cyclomatic_complexity(file_path)
            
            # Simplified maintainability index calculation
            # Lower is better, scale 0-100
            if lines == 0:
                return 100.0
            
            # Penalize long files and high complexity
            length_penalty = min(lines / 100, 1.0) * 30
            complexity_penalty = min(complexity / 10, 1.0) * 40
            
            maintainability = max(0, 100 - length_penalty - complexity_penalty)
            return round(maintainability, 2)
        except Exception:
            return 50.0
    
    async def _calculate_technical_debt(self, file_path: str) -> float:
        """Calculate technical debt (simplified)"""
        try:
            lines = await self._count_lines_of_code(file_path)
            complexity = await self._calculate_cyclomatic_complexity(file_path)
            
            # Simple technical debt calculation
            # Based on complexity and file size
            debt = (complexity * 0.5) + (lines * 0.01)
            return round(debt, 2)
        except Exception:
            return 0.0
    
    async def _calculate_code_coverage(self, file_path: str) -> float:
        """Calculate code coverage (placeholder - would need actual coverage data)"""
        # This would typically integrate with coverage tools
        # For now, return a placeholder value
        return 75.0
    
    async def _find_python_files(self, repo_path: str) -> List[str]:
        """Find all Python files in the repository"""
        python_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common non-code directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files
    
    async def _analyze_file_smells(self, file_path: str, sensitivity_level: str) -> List[Dict[str, Any]]:
        """Analyze a file for code smells"""
        smells = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Long method detection
            if len(lines) > 50 and sensitivity_level in ["medium", "high"]:
                smells.append({
                    "type": "long_method",
                    "severity": "medium",
                    "file_path": file_path,
                    "line_number": 1,
                    "description": f"Method is {len(lines)} lines long (threshold: 50)",
                    "suggestion": "Consider breaking this method into smaller functions"
                })
            
            # Long parameter list detection
            for i, line in enumerate(lines):
                if 'def ' in line and len(line.split(',')) > 5:
                    smells.append({
                        "type": "long_parameter_list",
                        "severity": "low",
                        "file_path": file_path,
                        "line_number": i + 1,
                        "description": "Function has many parameters",
                        "suggestion": "Consider using a data structure or configuration object"
                    })
            
            # Duplicate code detection (simplified)
            if sensitivity_level == "high":
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        # Count occurrences of this line
                        occurrences = sum(1 for l in lines if l.strip() == stripped)
                        if occurrences > 3:
                            smells.append({
                                "type": "duplicate_code",
                                "severity": "medium",
                                "file_path": file_path,
                                "line_number": i + 1,
                                "description": f"Duplicate code found ({occurrences} occurrences)",
                                "suggestion": "Extract common code into a function"
                            })
                            break
            
        except Exception as e:
            logger.warning(f"Error analyzing smells in {file_path}: {e}")
        
        return smells
    
    async def _get_commit_lines_changed(self, repo_path: str, commit_hash: str) -> Dict[str, int]:
        """Get lines added and removed for a commit"""
        try:
            cmd = ["git", "show", "--stat", "--format=", commit_hash]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                return {"added": 0, "removed": 0}
            
            # Parse the stat output
            added = 0
            removed = 0
            
            for line in result.stdout.split('\n'):
                if 'insertion' in line or 'deletion' in line:
                    # Extract numbers from lines like "2 files changed, 10 insertions(+), 5 deletions(-)"
                    numbers = re.findall(r'(\d+)', line)
                    if len(numbers) >= 2:
                        added += int(numbers[1])
                    if len(numbers) >= 3:
                        removed += int(numbers[2])
            
            return {"added": added, "removed": removed}
        except Exception:
            return {"added": 0, "removed": 0}
    
    async def _get_file_metrics(self, repo_path: str, file_path: str) -> Dict[str, Any]:
        """Get metrics for a specific file"""
        try:
            full_path = os.path.join(repo_path, file_path)
            if not os.path.exists(full_path):
                return {}
            
            lines = await self._count_lines_of_code(full_path)
            complexity = await self._calculate_cyclomatic_complexity(full_path)
            maintainability = await self._calculate_maintainability_index(full_path)
            
            return {
                "lines_of_code": lines,
                "cyclomatic_complexity": complexity,
                "maintainability_index": maintainability
            }
        except Exception:
            return {}
    
    async def _get_last_commit_date(self) -> str:
        """Get the date of the last commit"""
        try:
            result = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=iso"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"
    
    async def _generate_summary(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the analysis"""
        summary = {
            "overview": "Git repository analysis completed",
            "key_metrics": {},
            "recommendations": []
        }
        
        # Add key metrics
        if "code_metrics" in analysis_data:
            metrics = analysis_data["code_metrics"]
            summary["key_metrics"]["total_files"] = metrics.get("total_files", 0)
            summary["key_metrics"]["total_lines"] = metrics.get("total_lines_of_code", 0)
            summary["key_metrics"]["average_complexity"] = metrics.get("average_complexity", 0)
        
        if "code_smells" in analysis_data:
            smells = analysis_data["code_smells"]
            summary["key_metrics"]["total_smells"] = smells.get("total_smells", 0)
        
        if "contributors" in analysis_data:
            contributors = analysis_data["contributors"]
            summary["key_metrics"]["total_contributors"] = contributors.get("total_contributors", 0)
            summary["key_metrics"]["total_commits"] = contributors.get("total_commits", 0)
        
        # Add recommendations
        if "code_smells" in analysis_data and analysis_data["code_smells"].get("total_smells", 0) > 10:
            summary["recommendations"].append("High number of code smells detected. Consider refactoring.")
        
        if "code_metrics" in analysis_data:
            avg_complexity = analysis_data["code_metrics"].get("average_complexity", 0)
            if avg_complexity > 10:
                summary["recommendations"].append("High average cyclomatic complexity. Consider simplifying functions.")
        
        return summary

# MCP Server implementation
class MCPServer:
    """MCP Server for Git Analyzer"""
    
    def __init__(self):
        self.analyzer = GitAnalyzerServer()
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "analyze_repository":
                    result = await self.analyzer.analyze_repository(
                        arguments.get("repo_path", "."),
                        arguments.get("branch", "main"),
                        arguments.get("depth", 100)
                    )
                elif tool_name == "get_code_metrics":
                    result = await self.analyzer.get_code_metrics(
                        arguments.get("file_path"),
                        arguments.get("metric_types", [])
                    )
                elif tool_name == "detect_smells":
                    result = await self.analyzer.detect_smells(
                        arguments.get("repo_path", "."),
                        arguments.get("sensitivity_level", "medium")
                    )
                elif tool_name == "analyze_contributors":
                    result = await self.analyzer.analyze_contributors(
                        arguments.get("repo_path", "."),
                        arguments.get("time_range", "1 year")
                    )
                elif tool_name == "get_hotspots":
                    result = await self.analyzer.get_hotspots(
                        arguments.get("repo_path", "."),
                        arguments.get("threshold", 0.8)
                    )
                elif tool_name == "generate_report":
                    result = await self.analyzer.generate_report(
                        arguments.get("analysis_id"),
                        arguments.get("format", "json"),
                        arguments.get("sections", [])
                    )
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -32601, "message": "Method not found"}
                    }
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": "Method not found"}
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32603, "message": str(e)}
            }

async def main():
    """Main server loop"""
    server = MCPServer()
    
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
