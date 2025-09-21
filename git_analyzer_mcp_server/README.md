# Git Analyzer MCP Server

Servidor MCP para análisis de repositorios Git. **Solo 3 archivos necesarios.**

## 📁 Archivos

```
git_analyzer_client.py      # Cliente MCP
git_analyzer_executor.py    # Ejecutor de comandos  
git_analyzer_server.py      # Servidor MCP
```

## 🚀 Implementación en tu Chatbot

### 1. Copiar archivos
```bash
cp git_analyzer_client.py tu_proyecto/
cp git_analyzer_executor.py tu_proyecto/
cp git_analyzer_server.py tu_proyecto/
```

### 2. Agregar a tu código
```python
from git_analyzer_client import GitAnalyzerClient
from git_analyzer_executor import GitAnalyzerExecutor

class TuChatbot:
    def __init__(self):
        self.git_analyzer_client = GitAnalyzerClient()
        self.git_analyzer_executor = GitAnalyzerExecutor(self.git_analyzer_client)
    
    async def inicializar(self):
        await self.git_analyzer_client.start_analyzer_server()
    
    async def procesar_mensaje(self, mensaje: str) -> str:
        # Detectar comandos Git Analyzer
        if mensaje.lower() == "analyze repository":
            intencion = {"action": "analyze_repository", "repo_path": ".", "branch": "main", "depth": 100}
            return await self.git_analyzer_executor.execute_git_analyzer_intent(intencion, mensaje)
        
        # ... resto de tu lógica
```

## 📋 Comandos Disponibles

- `analyze repository` - Análisis completo
- `get code metrics <archivo>` - Métricas de archivo
- `detect smells` - Code smells
- `analyze contributors` - Contribuidores
- `get hotspots` - Archivos problemáticos

## 🧪 Probar

```bash
python3 ejemplo_integracion.py
```

## 📖 Ver Ejemplo Completo

Lee `ejemplo_integracion.py` para ver implementación completa.

## ✅ ¡Listo!

Con estos 3 archivos ya tienes Git Analyzer funcionando.