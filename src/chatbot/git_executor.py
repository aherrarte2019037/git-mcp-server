"""
Git Executor for Direct Git Operations
Executes Git intents using direct Git commands
"""
import logging
import subprocess
import os
from typing import Dict

class GitExecutor:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.logger = logging.getLogger(__name__)
    
    async def execute_git_intent(self, intent: Dict, original_message: str) -> str:
        """Execute Git intent based on detected action"""
        action = intent.get("action")
        repo_path = intent.get("repo_path", ".")
        files = intent.get("files", [])
        message = intent.get("message", "")
        max_count = intent.get("max_count", 10)
        
        # Log only the action being executed
        self.logger.info(f"Executing Git action: {action}")
        
        if action == "status":
            result = await self.mcp_client.git_status(repo_path)
            if result["success"]:
                status_data = result['data'].get('content', [{}])[0].get('text', 'No status information')
                return f"📊 Git Status:\n{status_data}"
            else:
                return f"❌ Error getting Git status: {result['error']}"
        
        elif action == "add":
            if not files:
                return "❌ No files specified to add"
            result = await self.mcp_client.git_add(repo_path, files)
            if result["success"]:
                return f"✅ Files added to staging: {', '.join(files)}"
            else:
                return f"❌ Error adding files: {result['error']}"
        
        elif action == "commit":
            if not message:
                return "❌ No commit message provided"
            result = await self.mcp_client.git_commit(repo_path, message)
            if result["success"]:
                commit_data = result['data'].get('content', [{}])[0].get('text', 'Commit created')
                return f"✅ Commit created:\n{commit_data}"
            else:
                return f"❌ Error creating commit: {result['error']}"
        
        elif action == "log":
            result = await self.mcp_client.git_log(repo_path, max_count)
            if result["success"]:
                log_data = result['data'].get('content', [{}])[0].get('text', 'No commits found')
                return f"📋 Git Log (last {max_count} commits):\n{log_data}"
            else:
                return f"❌ Error getting Git log: {result['error']}"
        
        elif action == "init":
            result = await self.mcp_client.git_init(repo_path)
            if result["success"]:
                init_data = result['data'].get('content', [{}])[0].get('text', 'Repository initialized')
                return f"✅ Git repository initialized:\n{init_data}"
            else:
                return f"❌ Error initializing Git repository: {result['error']}"
        
        elif action == "branch":
            result = await self.mcp_client.git_branch(repo_path)
            if result["success"]:
                branch_data = result['data'].get('content', [{}])[0].get('text', 'No branches found')
                return f"🌿 Git Branches:\n{branch_data}"
            else:
                return f"❌ Error listing branches: {result['error']}"
        
        return "❌ Acción Git no reconocida"
