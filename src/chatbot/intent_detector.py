"""
Intent Detector for MCP Filesystem Operations
Uses LLM to detect filesystem intents from natural language
"""
import json
import logging
from typing import Dict, Optional

class IntentDetector:
    def __init__(self, anthropic_client):
        self.anthropic_client = anthropic_client
        self.logger = logging.getLogger(__name__)
    
    async def detect_filesystem_intent(self, message: str) -> Optional[Dict]:
        """Detect filesystem intent using LLM"""
        try:
            # Check for fixed commands first
            message_lower = message.lower().strip()
            
            # Fixed command patterns
            if message_lower in ["list files", "ls"]:
                return {"action": "list", "path": "."}
            elif message_lower.startswith("read file "):
                file_path = message[10:].strip()
                return {"action": "read", "path": file_path}
            elif message_lower.startswith("write file "):
                parts = message[11:].strip().split(" ", 1)
                if len(parts) >= 1:
                    file_path = parts[0]
                    content = parts[1] if len(parts) > 1 else "Hello from MCP!"
                    return {"action": "write", "path": file_path, "content": content}
            
            # Create a system prompt for intent detection
            system_prompt = """Eres un detector de intenciones para operaciones de archivos. Tu única función es detectar si un mensaje del usuario solicita una operación de archivos y devolver un JSON específico.

HERRAMIENTAS DISPONIBLES:
- list_directory: Listar archivos en un directorio
- read_file: Leer el contenido de un archivo  
- write_file: Crear o escribir en un archivo

INSTRUCCIONES:
1. Analiza el mensaje del usuario
2. Si solicita operaciones de archivos, devuelve JSON
3. Si NO solicita operaciones de archivos, devuelve "null"
4. NO des explicaciones, solo devuelve JSON o "null"

FORMATO DE RESPUESTA:
{
  "action": "list|read|write",
  "path": "ruta/del/archivo/o/directorio", 
  "content": "contenido solo para write"
}

EJEMPLOS:
- "muestra los archivos" → {"action": "list", "path": "."}
- "qué archivos hay" → {"action": "list", "path": "."}
- "lee README.md" → {"action": "read", "path": "README.md"}
- "crea test.txt con hola" → {"action": "write", "path": "test.txt", "content": "hola"}
- "hola como estas" → null
- "explica qué es Python" → null"""

            # Send to LLM for intent detection
            response = await self.anthropic_client.get_response(
                f"{system_prompt}\n\nMensaje del usuario: {message}",
                []
            )
            
            # Parse JSON response
            try:
                intent = json.loads(response.strip())
                if intent and isinstance(intent, dict) and "action" in intent:
                    return intent
            except json.JSONDecodeError:
                pass
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error detecting filesystem intent with LLM: {e}")
            return None
    
    async def detect_git_intent(self, message: str) -> Optional[Dict]:
        """Detect Git intent using LLM"""
        try:
            # Check for fixed commands first
            message_lower = message.lower().strip()
            
            # Fixed command patterns
            if message_lower == "git status":
                return {"action": "status", "repo_path": "."}
            elif message_lower.startswith("git add "):
                files = message[8:].strip().split()
                return {"action": "add", "repo_path": ".", "files": files}
            elif message_lower.startswith("git commit "):
                message_text = message[11:].strip()
                return {"action": "commit", "repo_path": ".", "message": message_text}
            elif message_lower == "git log":
                return {"action": "log", "repo_path": ".", "max_count": 10}
            elif message_lower == "git init":
                return {"action": "init", "repo_path": "."}
            elif message_lower == "git branch":
                return {"action": "branch", "repo_path": "."}
            
            # Create a system prompt for Git intent detection
            system_prompt = """Eres un detector de intenciones para operaciones Git. Tu única función es detectar si un mensaje del usuario solicita una operación Git y devolver un JSON específico.

HERRAMIENTAS DISPONIBLES:
- git_status: Ver el estado del repositorio
- git_add: Agregar archivos al staging
- git_commit: Crear un commit
- git_log: Ver el historial de commits
- git_init: Inicializar un repositorio Git
- git_branch: Listar ramas

INSTRUCCIONES:
1. Analiza el mensaje del usuario
2. Si solicita operaciones Git, devuelve JSON
3. Si NO solicita operaciones Git, devuelve "null"
4. NO des explicaciones, solo devuelve JSON o "null"

FORMATO DE RESPUESTA:
{
  "action": "status|add|commit|log|init|branch",
  "repo_path": "ruta/del/repositorio",
  "files": ["archivo1.txt", "archivo2.txt"] (solo para add),
  "message": "mensaje del commit" (solo para commit),
  "max_count": 10 (solo para log)
}

EJEMPLOS:
- "muestra el estado de git" → {"action": "status", "repo_path": "."}
- "agrega README.md" → {"action": "add", "repo_path": ".", "files": ["README.md"]}
- "haz commit con mensaje inicial" → {"action": "commit", "repo_path": ".", "message": "mensaje inicial"}
- "muestra el log de git" → {"action": "log", "repo_path": ".", "max_count": 10}
- "inicializa git" → {"action": "init", "repo_path": "."}
- "hola como estas" → null
- "explica qué es Python" → null"""

            # Send to LLM for intent detection
            response = await self.anthropic_client.get_response(
                f"{system_prompt}\n\nMensaje del usuario: {message}",
                []
            )
            
            # Parse JSON response
            try:
                intent = json.loads(response.strip())
                if intent and isinstance(intent, dict) and "action" in intent:
                    return intent
            except json.JSONDecodeError:
                pass
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error detecting Git intent with LLM: {e}")
            return None
