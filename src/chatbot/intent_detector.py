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
