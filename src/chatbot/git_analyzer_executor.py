"""
Git Analyzer Executor for MCP Operations
Executes Git Analyzer intents detected by the IntentDetector
"""
import logging
from typing import Dict

class GitAnalyzerExecutor:
    def __init__(self, git_analyzer_client):
        self.git_analyzer_client = git_analyzer_client
        self.logger = logging.getLogger(__name__)
    
    async def execute_git_analyzer_intent(self, intent: Dict, original_message: str) -> str:
        """Execute Git Analyzer intent based on detected action"""
        action = intent.get("action")
        repo_path = intent.get("repo_path", ".")
        branch = intent.get("branch", "main")
        depth = intent.get("depth", 100)
        file_path = intent.get("file_path", "")
        metric_types = intent.get("metric_types", [])
        sensitivity_level = intent.get("sensitivity_level", "medium")
        time_range = intent.get("time_range", "1 year")
        threshold = intent.get("threshold", 0.8)
        analysis_id = intent.get("analysis_id", "")
        format_type = intent.get("format", "json")
        sections = intent.get("sections", [])
        
        # Log only the action being executed
        self.logger.info(f"Executing Git Analyzer action: {action}")
        
        if action == "analyze_repository":
            result = await self.git_analyzer_client.analyze_repository(repo_path, branch, depth)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    analysis_data = data["data"]
                    analysis_id = data.get("analysis_id", "unknown")
                else:
                    analysis_data = data
                    analysis_id = analysis_data.get("analysis_id", "unknown")
                
                summary = f"🔍 **Repository Analysis Complete**\n"
                summary += f"📊 **Analysis ID:** {analysis_id}\n"
                summary += f"🌿 **Branch:** {analysis_data.get('branch', 'main')}\n"
                summary += f"📅 **Analyzed:** {analysis_data.get('analysis_timestamp', 'unknown')}\n\n"
                
                # Repository info
                if "repository_info" in analysis_data:
                    repo_info = analysis_data["repository_info"]
                    summary += f"📈 **Repository Info:**\n"
                    summary += f"  • Current Branch: {repo_info.get('current_branch', 'unknown')}\n"
                    summary += f"  • Total Commits: {repo_info.get('total_commits', 0)}\n"
                    summary += f"  • Repository Size: {repo_info.get('repository_size', 'unknown')}\n\n"
                
                # Code metrics
                if "code_metrics" in analysis_data:
                    metrics = analysis_data["code_metrics"]
                    summary += f"📊 **Code Metrics:**\n"
                    summary += f"  • Files Analyzed: {metrics.get('total_files', 0)}\n"
                    summary += f"  • Total Lines: {metrics.get('total_lines_of_code', 0)}\n"
                    summary += f"  • Avg Complexity: {metrics.get('average_complexity', 0):.2f}\n"
                    summary += f"  • Lines per File: {metrics.get('lines_per_file', 0):.1f}\n\n"
                
                # Code smells
                if "code_smells" in analysis_data:
                    smells = analysis_data["code_smells"]
                    summary += f"🚨 **Code Smells:**\n"
                    summary += f"  • Total Smells: {smells.get('total_smells', 0)}\n"
                    summary += f"  • Files Analyzed: {smells.get('files_analyzed', 0)}\n\n"
                
                # Contributors
                if "contributors" in analysis_data:
                    contributors = analysis_data["contributors"]
                    summary += f"👥 **Contributors:**\n"
                    summary += f"  • Total Contributors: {contributors.get('total_contributors', 0)}\n"
                    summary += f"  • Total Commits: {contributors.get('total_commits', 0)}\n\n"
                
                # Hotspots
                if "hotspots" in analysis_data:
                    hotspots = analysis_data["hotspots"]
                    summary += f"🔥 **Hotspots:**\n"
                    summary += f"  • Problematic Files: {len(hotspots.get('hotspots', []))}\n"
                    summary += f"  • Threshold: {hotspots.get('threshold', 0.8)}\n\n"
                
                summary += f"💡 **Use 'generate report {analysis_id}' to get detailed report**"
                
                return summary
            else:
                return f"❌ Error analyzing repository: {result['error']}"
        
        elif action == "get_code_metrics":
            if not file_path:
                return "❌ No file path specified"
            
            result = await self.git_analyzer_client.get_code_metrics(file_path, metric_types)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    metrics_data = data["data"]
                else:
                    metrics_data = data
                
                summary = f"📊 **Code Metrics for {file_path}:**\n\n"
                
                for metric, value in metrics_data.items():
                    if isinstance(value, float):
                        summary += f"  • {metric.replace('_', ' ').title()}: {value:.2f}\n"
                    else:
                        summary += f"  • {metric.replace('_', ' ').title()}: {value}\n"
                
                return summary
            else:
                return f"❌ Error getting code metrics: {result['error']}"
        
        elif action == "detect_smells":
            result = await self.git_analyzer_client.detect_smells(repo_path, sensitivity_level)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    smells_data = data["data"]
                else:
                    smells_data = data
                
                summary = f"🚨 **Code Smells Detection:**\n\n"
                summary += f"📊 **Summary:**\n"
                summary += f"  • Total Smells: {smells_data.get('total_smells', 0)}\n"
                summary += f"  • Files Analyzed: {smells_data.get('files_analyzed', 0)}\n"
                summary += f"  • Sensitivity: {smells_data.get('sensitivity_level', 'medium')}\n\n"
                
                # Show smells by type
                smells_by_type = smells_data.get('smells_by_type', {})
                if smells_by_type:
                    summary += f"📋 **Smells by Type:**\n"
                    for smell_type, smells in smells_by_type.items():
                        summary += f"  • {smell_type.replace('_', ' ').title()}: {len(smells)} occurrences\n"
                    
                    # Show some examples
                    summary += f"\n🔍 **Examples:**\n"
                    count = 0
                    for smell_type, smells in smells_by_type.items():
                        for smell in smells[:2]:  # Show first 2 of each type
                            summary += f"  • {smell['file_path']}:{smell['line_number']} - {smell['description']}\n"
                            count += 1
                            if count >= 5:  # Limit examples
                                break
                        if count >= 5:
                            break
                
                return summary
            else:
                return f"❌ Error detecting smells: {result['error']}"
        
        elif action == "analyze_contributors":
            result = await self.git_analyzer_client.analyze_contributors(repo_path, time_range)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    contributors_data = data["data"]
                else:
                    contributors_data = data
                
                summary = f"👥 **Contributor Analysis:**\n\n"
                summary += f"📊 **Summary:**\n"
                summary += f"  • Total Contributors: {contributors_data.get('total_contributors', 0)}\n"
                summary += f"  • Total Commits: {contributors_data.get('total_commits', 0)}\n"
                summary += f"  • Time Range: {contributors_data.get('time_range', '1 year')}\n\n"
                
                # Show top contributors
                contributors = contributors_data.get('contributors', [])
                if contributors:
                    summary += f"🏆 **Top Contributors:**\n"
                    for i, contributor in enumerate(contributors[:5]):  # Top 5
                        summary += f"  {i+1}. {contributor['name']} ({contributor['email']})\n"
                        summary += f"     • Commits: {contributor['commits']}\n"
                        summary += f"     • Lines Added: {contributor['lines_added']}\n"
                        summary += f"     • Lines Removed: {contributor['lines_removed']}\n"
                        summary += f"     • Ownership: {contributor['ownership_percentage']:.1f}%\n\n"
                
                return summary
            else:
                return f"❌ Error analyzing contributors: {result['error']}"
        
        elif action == "get_hotspots":
            result = await self.git_analyzer_client.get_hotspots(repo_path, threshold)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    hotspots_data = data["data"]
                else:
                    hotspots_data = data
                
                summary = f"🔥 **Code Hotspots:**\n\n"
                summary += f"📊 **Summary:**\n"
                summary += f"  • Hotspots Found: {len(hotspots_data.get('hotspots', []))}\n"
                summary += f"  • Threshold: {hotspots_data.get('threshold', 0.8)}\n"
                summary += f"  • Files Analyzed: {hotspots_data.get('total_files_analyzed', 0)}\n\n"
                
                # Show hotspots
                hotspots = hotspots_data.get('hotspots', [])
                if hotspots:
                    summary += f"🔥 **Problematic Files:**\n"
                    for i, hotspot in enumerate(hotspots[:5]):  # Top 5
                        summary += f"  {i+1}. {hotspot['file_path']}\n"
                        summary += f"     • Change Frequency: {hotspot['change_frequency']:.2%}\n"
                        summary += f"     • Total Changes: {hotspot['total_changes']}\n"
                        
                        # Show metrics if available
                        metrics = hotspot.get('metrics', {})
                        if metrics:
                            summary += f"     • Lines of Code: {metrics.get('lines_of_code', 'N/A')}\n"
                            summary += f"     • Complexity: {metrics.get('cyclomatic_complexity', 'N/A')}\n"
                        summary += "\n"
                
                return summary
            else:
                return f"❌ Error getting hotspots: {result['error']}"
        
        elif action == "generate_report":
            if not analysis_id:
                return "❌ No analysis ID specified"
            
            result = await self.git_analyzer_client.generate_report(analysis_id, format_type, sections)
            if result["success"]:
                data = result["data"]
                # Handle nested data structure
                if "data" in data:
                    report_data = data["data"]
                else:
                    report_data = data
                
                summary = f"📋 **Analysis Report Generated:**\n\n"
                summary += f"📊 **Report Info:**\n"
                summary += f"  • Report ID: {report_data.get('report_id', 'unknown')}\n"
                summary += f"  • Analysis ID: {report_data.get('analysis_id', 'unknown')}\n"
                summary += f"  • Format: {report_data.get('format', 'json')}\n"
                summary += f"  • Generated: {report_data.get('generated_at', 'unknown')}\n"
                summary += f"  • Sections: {', '.join(report_data.get('sections', []))}\n\n"
                
                # Show summary if available
                if "summary" in report_data:
                    summary_data = report_data["summary"]
                    summary += f"📈 **Summary:**\n"
                    summary += f"  • {summary_data.get('overview', 'Analysis completed')}\n\n"
                    
                    # Key metrics
                    key_metrics = summary_data.get('key_metrics', {})
                    if key_metrics:
                        summary += f"📊 **Key Metrics:**\n"
                        for metric, value in key_metrics.items():
                            summary += f"  • {metric.replace('_', ' ').title()}: {value}\n"
                        summary += "\n"
                    
                    # Recommendations
                    recommendations = summary_data.get('recommendations', [])
                    if recommendations:
                        summary += f"💡 **Recommendations:**\n"
                        for rec in recommendations:
                            summary += f"  • {rec}\n"
                
                return summary
            else:
                return f"❌ Error generating report: {result['error']}"
        
        return "❌ Acción Git Analyzer no reconocida"
