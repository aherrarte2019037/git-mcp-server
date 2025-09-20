"""
Filesystem Executor for MCP Operations
Executes filesystem intents detected by the IntentDetector
"""
import logging
from typing import Dict

class FilesystemExecutor:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.logger = logging.getLogger(__name__)
    
    async def execute_filesystem_intent(self, intent: Dict, original_message: str) -> str:
        """Execute filesystem intent based on detected action"""
        action = intent.get("action")
        path = intent.get("path", ".")
        content = intent.get("content", "")
        
        # Log only the action being executed
        self.logger.info(f"Executing filesystem action: {action}")
        
        if action == "list":
            result = await self.mcp_client.filesystem_list_files(path)
            if result["success"]:
                files_data = result['data'].get('content', [{}])[0].get('text', 'No files found')
                return f"📁 Archivos en {path}:\n{files_data}"
            else:
                return f"❌ Error listando archivos: {result['error']}"
        
        elif action == "read":
            result = await self.mcp_client.filesystem_read_file(path)
            if result["success"]:
                file_content = result['data'].get('content', [{}])[0].get('text', 'Archivo vacío')
                return f"📄 Contenido de {path}:\n{file_content}"
            else:
                return f"❌ Error leyendo archivo: {result['error']}"
        
        elif action == "write":
            if not content:
                content = "Archivo creado desde MCP"
            result = await self.mcp_client.filesystem_write_file(path, content)
            if result["success"]:
                return f"✅ Archivo creado exitosamente: {path}"
            else:
                return f"❌ Error creando archivo: {result['error']}"
        
        return "❌ Acción no reconocida"
