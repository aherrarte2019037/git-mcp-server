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
    
    async def detect_git_analyzer_intent(self, message: str) -> Optional[Dict]:
        """Detect Git Analyzer intent using LLM"""
        try:
            # Check for fixed commands first
            message_lower = message.lower().strip()
            
            # Fixed command patterns for Git Analyzer
            if message_lower == "analyze repository":
                return {"action": "analyze_repository", "repo_path": ".", "branch": "main", "depth": 100}
            elif message_lower.startswith("analyze repository "):
                parts = message[18:].strip().split()
                repo_path = parts[0] if parts else "."
                return {"action": "analyze_repository", "repo_path": repo_path, "branch": "main", "depth": 100}
            elif message_lower.startswith("get code metrics "):
                file_path = message[17:].strip()
                return {"action": "get_code_metrics", "file_path": file_path}
            elif message_lower == "detect smells":
                return {"action": "detect_smells", "repo_path": ".", "sensitivity_level": "medium"}
            elif message_lower.startswith("detect smells "):
                parts = message[14:].strip().split()
                repo_path = parts[0] if parts else "."
                return {"action": "detect_smells", "repo_path": repo_path, "sensitivity_level": "medium"}
            elif message_lower == "analyze contributors":
                return {"action": "analyze_contributors", "repo_path": ".", "time_range": "1 year"}
            elif message_lower.startswith("analyze contributors "):
                parts = message[20:].strip().split()
                repo_path = parts[0] if parts else "."
                return {"action": "analyze_contributors", "repo_path": repo_path, "time_range": "1 year"}
            elif message_lower == "get hotspots":
                return {"action": "get_hotspots", "repo_path": ".", "threshold": 0.8}
            elif message_lower.startswith("get hotspots "):
                parts = message[12:].strip().split()
                repo_path = parts[0] if parts else "."
                return {"action": "get_hotspots", "repo_path": repo_path, "threshold": 0.8}
            elif message_lower.startswith("generate report "):
                analysis_id = message[16:].strip()
                return {"action": "generate_report", "analysis_id": analysis_id}
            
            # Create a system prompt for Git Analyzer intent detection
            system_prompt = """Eres un detector de intenciones para operaciones de Git Analyzer. Tu única función es detectar si un mensaje del usuario solicita una operación de análisis de código y devolver un JSON específico.

HERRAMIENTAS DISPONIBLES:
- analyze_repository: Análisis completo del repositorio
- get_code_metrics: Obtiene métricas de calidad del código
- detect_smells: Detecta code smells y antipatrones
- analyze_contributors: Análisis de contribuciones y ownership
- get_hotspots: Identifica archivos problemáticos
- generate_report: Genera reporte comprehensivo

INSTRUCCIONES:
1. Analiza el mensaje del usuario
2. Si solicita operaciones de Git Analyzer, devuelve JSON
3. Si NO solicita operaciones de Git Analyzer, devuelve "null"
4. NO des explicaciones, solo devuelve JSON o "null"

FORMATO DE RESPUESTA:
{
  "action": "analyze_repository|get_code_metrics|detect_smells|analyze_contributors|get_hotspots|generate_report",
  "repo_path": "ruta/del/repositorio",
  "file_path": "ruta/del/archivo" (solo para get_code_metrics),
  "branch": "main" (solo para analyze_repository),
  "depth": 100 (solo para analyze_repository),
  "metric_types": ["lines_of_code", "cyclomatic_complexity"] (solo para get_code_metrics),
  "sensitivity_level": "medium" (solo para detect_smells),
  "time_range": "1 year" (solo para analyze_contributors),
  "threshold": 0.8 (solo para get_hotspots),
  "analysis_id": "analysis_123" (solo para generate_report),
  "format": "json" (solo para generate_report),
  "sections": ["repository_info", "code_metrics"] (solo para generate_report)
}

EJEMPLOS:
- "analiza el repositorio" → {"action": "analyze_repository", "repo_path": ".", "branch": "main", "depth": 100}
- "obtén métricas del archivo main.py" → {"action": "get_code_metrics", "file_path": "main.py"}
- "detecta code smells" → {"action": "detect_smells", "repo_path": ".", "sensitivity_level": "medium"}
- "analiza contribuidores" → {"action": "analyze_contributors", "repo_path": ".", "time_range": "1 year"}
- "obtén hotspots" → {"action": "get_hotspots", "repo_path": ".", "threshold": 0.8}
- "genera reporte analysis_123" → {"action": "generate_report", "analysis_id": "analysis_123"}
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
            self.logger.error(f"Error detecting Git Analyzer intent with LLM: {e}")
            return None
    
    async def detect_weather_intent(self, message: str) -> Optional[Dict]:
        """Detect Weather intent using LLM"""
        try:
            # Check for fixed commands first
            message_lower = message.lower().strip()
            
            # Fixed command patterns for Weather
            if message_lower.startswith("weather in "):
                city = message[11:].strip()
                return {"action": "weather", "city": city}
            elif message_lower.startswith("clima en "):
                city = message[9:].strip()
                return {"action": "weather", "city": city}
            elif message_lower.startswith("forecast in "):
                city = message[12:].strip()
                return {"action": "forecast", "city": city, "days": 3}
            elif message_lower.startswith("pronóstico en "):
                city = message[14:].strip()
                return {"action": "forecast", "city": city, "days": 3}
            elif message_lower.startswith("weather alerts in "):
                city = message[18:].strip()
                return {"action": "alerts", "city": city}
            elif message_lower.startswith("alertas en "):
                city = message[11:].strip()
                return {"action": "alerts", "city": city}
            
            # Create a system prompt for Weather intent detection
            system_prompt = """Eres un detector de intenciones para operaciones de clima. Tu única función es detectar si un mensaje del usuario solicita información del clima y devolver un JSON específico.

HERRAMIENTAS DISPONIBLES:
- get_weather: Obtener clima actual de una ciudad
- get_forecast: Obtener pronóstico del clima para los próximos días
- get_weather_alerts: Obtener alertas meteorológicas para una ciudad

INSTRUCCIONES:
1. Analiza el mensaje del usuario
2. Si solicita información del clima, devuelve JSON
3. Si NO solicita información del clima, devuelve "null"
4. NO des explicaciones, solo devuelve JSON o "null"

FORMATO DE RESPUESTA:
{
  "action": "weather|forecast|alerts",
  "city": "nombre de la ciudad",
  "days": 3 (solo para forecast)
}

EJEMPLOS:
- "¿qué clima hace en Madrid?" → {"action": "weather", "city": "Madrid"}
- "clima en Barcelona" → {"action": "weather", "city": "Barcelona"}
- "pronóstico para París" → {"action": "forecast", "city": "París", "days": 3}
- "forecast for London 5 days" → {"action": "forecast", "city": "London", "days": 5}
- "alertas meteorológicas en Sevilla" → {"action": "alerts", "city": "Sevilla"}
- "weather alerts in New York" → {"action": "alerts", "city": "New York"}
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
            self.logger.error(f"Error detecting Weather intent with LLM: {e}")
            return None
