# 🔍 Git Analyzer MCP Server

## 📋 Descripción

Servidor MCP (Model Context Protocol) especializado en análisis profundo de repositorios Git. Proporciona métricas avanzadas de calidad de código, detección de patrones problemáticos, análisis de contribuciones y generación de reportes comprehensivos.

## 🚀 Características

- **Análisis multi-dimensional**: Examina código, historia, contribuciones y patrones
- **Algoritmos complejos**: Detección de code smells, complejidad ciclomática, análisis de acoplamiento
- **Procesamiento de datos masivos**: Capaz de analizar repositorios con miles de commits
- **Inteligencia contextual**: Genera recomendaciones personalizadas
- **Integración con herramientas externas**: Conecta con linters especializados

## 🛠️ Instalación

### Requisitos
- Python 3.8+
- Git instalado en el sistema
- Acceso a un repositorio Git

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd git-analyzer-mcp-server

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python server.py
```

## 📡 Especificación del Servidor

### **Transporte**: STDIO
### **Protocolo**: JSON-RPC 2.0
### **Puerto**: N/A (comunicación por stdin/stdout)

## 🔧 Herramientas Disponibles

### 1. **analyze_repository**
Analiza un repositorio completo y genera un reporte comprehensivo.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `include_metrics` (boolean, opcional): Incluir métricas de código (default: true)
- `include_smells` (boolean, opcional): Incluir detección de code smells (default: true)
- `include_contributors` (boolean, opcional): Incluir análisis de contribuidores (default: true)
- `include_hotspots` (boolean, opcional): Incluir análisis de hotspots (default: true)

**Respuesta:**
```json
{
  "data": {
    "repository_info": {
      "name": "nombre-del-repo",
      "path": "/ruta/al/repo",
      "total_commits": 150,
      "total_files": 45,
      "total_lines": 2500
    },
    "metrics": { ... },
    "smells": { ... },
    "contributors": { ... },
    "hotspots": { ... }
  }
}
```

### 2. **get_code_metrics**
Obtiene métricas específicas de calidad de código.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `metric_types` (array, opcional): Tipos de métricas a calcular
  - Valores: `["lines_of_code", "cyclomatic_complexity", "maintainability_index", "file_count"]`
  - Default: Todas las métricas disponibles

**Respuesta:**
```json
{
  "data": {
    "lines_of_code": 2500,
    "cyclomatic_complexity": 15.2,
    "maintainability_index": 78.5,
    "file_count": 45
  }
}
```

### 3. **detect_smells**
Detecta patrones problemáticos en el código.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `smell_types` (array, opcional): Tipos de smells a detectar
  - Valores: `["long_methods", "duplicate_code", "complex_conditionals", "large_classes"]`
  - Default: Todos los tipos

**Respuesta:**
```json
{
  "data": {
    "long_methods": [
      {
        "file": "src/main.py",
        "method": "process_data",
        "lines": 45,
        "complexity": 12
      }
    ],
    "duplicate_code": [ ... ],
    "complex_conditionals": [ ... ],
    "large_classes": [ ... ]
  }
}
```

### 4. **analyze_contributors**
Analiza la actividad y contribuciones de los desarrolladores.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `time_period` (string, opcional): Período de análisis
  - Valores: `"last_month"`, `"last_3_months"`, `"last_year"`, `"all_time"`
  - Default: `"all_time"`

**Respuesta:**
```json
{
  "data": {
    "total_contributors": 5,
    "active_contributors": 3,
    "contributors": [
      {
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "commits": 45,
        "lines_added": 1200,
        "lines_removed": 300,
        "files_changed": 25
      }
    ]
  }
}
```

### 5. **get_hotspots**
Identifica áreas de código con alta frecuencia de cambios.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `limit` (integer, opcional): Número máximo de hotspots a retornar (default: 10)

**Respuesta:**
```json
{
  "data": {
    "hotspots": [
      {
        "file": "src/core.py",
        "change_frequency": 0.85,
        "commits_affecting": 42,
        "lines_changed": 150
      }
    ]
  }
}
```

### 6. **generate_report**
Genera un reporte completo del análisis.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `format` (string, opcional): Formato del reporte
  - Valores: `"json"`, `"summary"`, `"detailed"`
  - Default: `"json"`

**Respuesta:**
```json
{
  "data": {
    "report": {
      "summary": "Resumen del análisis...",
      "recommendations": ["Recomendación 1", "Recomendación 2"],
      "score": 7.5,
      "details": { ... }
    }
  }
}
```

## 🔌 Integración con Chatbot

### Ejemplo de Uso
```python
from mcp_servers.git_analyzer_client import GitAnalyzerClient

# Inicializar cliente
client = GitAnalyzerClient()

# Analizar repositorio
result = await client.analyze_repository("/path/to/repo")

# Obtener métricas específicas
metrics = await client.get_code_metrics("/path/to/repo", ["lines_of_code", "cyclomatic_complexity"])

# Detectar code smells
smells = await client.detect_smells("/path/to/repo")
```

### Comandos del Chatbot
- `"analyze repository"` - Análisis completo
- `"get code metrics"` - Métricas de código
- `"detect smells"` - Detección de code smells
- `"analyze contributors"` - Análisis de contribuidores
- `"get hotspots"` - Identificar hotspots
- `"generate report"` - Generar reporte

## 📊 Métricas Disponibles

### **Líneas de Código**
- Total de líneas en el repositorio
- Líneas por archivo
- Distribución por tipo de archivo

### **Complejidad Ciclomática**
- Medida de complejidad del código
- Identificación de métodos complejos
- Recomendaciones de refactoring

### **Índice de Mantenibilidad**
- Puntuación de 0-100
- Factores: complejidad, duplicación, comentarios
- Recomendaciones de mejora

### **Code Smells**
- Métodos largos (>50 líneas)
- Código duplicado
- Condicionales complejas
- Clases grandes

## 🚨 Manejo de Errores

### Errores Comunes
- **Repository not found**: El repositorio no existe
- **Not a git repository**: La ruta no es un repositorio Git válido
- **Permission denied**: Sin permisos para acceder al repositorio
- **Analysis failed**: Error durante el análisis

### Códigos de Error
- `1001`: Repositorio no encontrado
- `1002`: No es un repositorio Git
- `1003`: Sin permisos de acceso
- `1004`: Error de análisis
- `1005`: Parámetros inválidos

## 📝 Logs y Debugging

### Nivel de Log
- **INFO**: Operaciones normales
- **WARNING**: Advertencias no críticas
- **ERROR**: Errores que impiden el funcionamiento
- **DEBUG**: Información detallada para debugging

### Archivos de Log
- `git_analyzer.log`: Log principal del servidor
- `analysis.log`: Log específico de análisis
- `errors.log`: Log de errores

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Nivel de log
export GIT_ANALYZER_LOG_LEVEL=INFO

# Timeout para análisis
export GIT_ANALYZER_TIMEOUT=300

# Directorio de cache
export GIT_ANALYZER_CACHE_DIR=/tmp/git_analyzer_cache
```

### Configuración del Servidor
```json
{
  "server": {
    "name": "git-analyzer-mcp",
    "version": "1.0.0",
    "timeout": 300,
    "max_file_size": 1048576,
    "cache_enabled": true
  }
}
```

## 📚 Ejemplos de Uso

### Análisis Básico
```bash
# Analizar repositorio completo
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "analyze_repository",
    "params": {
      "repo_path": "/path/to/repo"
    },
    "id": 1
  }'
```

### Análisis Específico
```bash
# Obtener solo métricas de código
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get_code_metrics",
    "params": {
      "repo_path": "/path/to/repo",
      "metric_types": ["lines_of_code", "cyclomatic_complexity"]
    },
    "id": 2
  }'
```

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama para feature
3. Implementar cambios
4. Agregar tests
5. Crear pull request

### Estándares de Código
- PEP 8 para Python
- Docstrings en todas las funciones
- Tests para nuevas funcionalidades
- Documentación actualizada

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 🆘 Soporte

### Documentación
- README principal del proyecto
- Documentación de la API
- Ejemplos de integración

### Contacto
- Issues en GitHub
- Email: soporte@example.com
- Discord: #git-analyzer-mcp

---

**Desarrollado para el curso CC3067 Redes - Universidad del Valle de Guatemala**
