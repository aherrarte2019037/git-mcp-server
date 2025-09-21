# 🔧 Git MCP Server

## 📋 Descripción

Servidor MCP (Model Context Protocol) oficial de Anthropic para operaciones de control de versiones Git. Permite interactuar con repositorios Git de forma segura desde aplicaciones de IA, incluyendo operaciones de commit, branch, log y más.

## 🚀 Características

- **Operaciones Git completas**: Status, add, commit, log, branch, checkout
- **Control de versiones**: Gestión completa de repositorios Git
- **Seguridad**: Acceso controlado a repositorios específicos
- **Estándar oficial**: Desarrollado por Anthropic
- **Alto rendimiento**: Optimizado para operaciones Git
- **Multiplataforma**: Compatible con Windows, macOS, Linux

## 🛠️ Instalación

### Requisitos
- Python 3.8+
- Git instalado en el sistema
- uv (recomendado) o pip

### Instalación con uv (Recomendado)
```bash
# Instalar uv si no está instalado
curl -LsSf https://astral.sh/uv/install.sh | sh

# Usar con uvx (no requiere instalación)
uvx mcp-server-git --repository /path/to/repo
```

### Instalación con pip
```bash
# Instalar globalmente
pip install mcp-server-git

# Ejecutar
python -m mcp_server_git --repository /path/to/repo
```

### Configuración con Claude Desktop
```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

## 📡 Especificación del Servidor

### **Transporte**: STDIO
### **Protocolo**: JSON-RPC 2.0
### **Puerto**: N/A (comunicación por stdin/stdout)
### **Desarrollador**: Anthropic

## 🔧 Herramientas Disponibles

### 1. **git_status**
Muestra el estado del directorio de trabajo.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_status",
  "params": {
    "repo_path": "/path/to/repo"
  },
  "id": 1
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "status": "On branch main\nYour branch is up to date with 'origin/main'.\n\nChanges not staged for commit:\n  (use \"git add <file>...\" to update what will be committed)\n  (use \"git restore <file>...\" to discard changes in working directory)\n\tmodified:   file.txt\n\nUntracked files:\n  (use \"git add <file>...\" to include in what will be committed)\n\tnew_file.txt\n\nno changes added to commit (use \"git add\" and/or \"git commit -a\")"
    }
  },
  "id": 1
}
```

### 2. **git_add**
Agrega archivos al área de staging.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `files` (array, requerido): Lista de archivos a agregar

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_add",
  "params": {
    "repo_path": "/path/to/repo",
    "files": ["file.txt", "new_file.txt"]
  },
  "id": 2
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "message": "Files added to staging area",
      "files": ["file.txt", "new_file.txt"]
    }
  },
  "id": 2
}
```

### 3. **git_commit**
Realiza un commit con los cambios staged.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `message` (string, requerido): Mensaje del commit

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_commit",
  "params": {
    "repo_path": "/path/to/repo",
    "message": "Add new features and fix bugs"
  },
  "id": 3
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "message": "Commit created successfully",
      "commit_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
      "author": "User <user@example.com>",
      "date": "2024-01-15T10:30:00Z"
    }
  },
  "id": 3
}
```

### 4. **git_log**
Muestra el historial de commits.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `max_count` (integer, opcional): Número máximo de commits a mostrar
  - Default: 10
- `start_timestamp` (string, opcional): Fecha de inicio para filtrar
- `end_timestamp` (string, opcional): Fecha de fin para filtrar

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_log",
  "params": {
    "repo_path": "/path/to/repo",
    "max_count": 5
  },
  "id": 4
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "commits": [
        {
          "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
          "author": "User <user@example.com>",
          "date": "2024-01-15T10:30:00Z",
          "message": "Add new features and fix bugs"
        },
        {
          "hash": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1",
          "author": "User <user@example.com>",
          "date": "2024-01-14T15:45:00Z",
          "message": "Initial commit"
        }
      ]
    }
  },
  "id": 4
}
```

### 5. **git_init**
Inicializa un nuevo repositorio Git.

**Parámetros:**
- `repo_path` (string, requerido): Ruta del directorio a inicializar

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_init",
  "params": {
    "repo_path": "/path/to/new/repo"
  },
  "id": 5
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "message": "Repository initialized successfully",
      "path": "/path/to/new/repo"
    }
  },
  "id": 5
}
```

### 6. **git_branch**
Lista las ramas del repositorio.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `branch_type` (string, opcional): Tipo de ramas a listar
  - Valores: `"local"`, `"remote"`, `"all"`
  - Default: `"all"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_branch",
  "params": {
    "repo_path": "/path/to/repo",
    "branch_type": "all"
  },
  "id": 6
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "branches": [
        {
          "name": "main",
          "type": "local",
          "current": true,
          "last_commit": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
        },
        {
          "name": "feature/new-feature",
          "type": "local",
          "current": false,
          "last_commit": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1"
        }
      ]
    }
  },
  "id": 6
}
```

### 7. **git_checkout**
Cambia a una rama específica.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `branch_name` (string, requerido): Nombre de la rama

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_checkout",
  "params": {
    "repo_path": "/path/to/repo",
    "branch_name": "feature/new-feature"
  },
  "id": 7
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "message": "Switched to branch 'feature/new-feature'",
      "branch": "feature/new-feature"
    }
  },
  "id": 7
}
```

### 8. **git_create_branch**
Crea una nueva rama.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `branch_name` (string, requerido): Nombre de la nueva rama
- `start_point` (string, opcional): Punto de inicio para la rama
  - Default: `"HEAD"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_create_branch",
  "params": {
    "repo_path": "/path/to/repo",
    "branch_name": "feature/new-feature",
    "start_point": "main"
  },
  "id": 8
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "message": "Branch 'feature/new-feature' created successfully",
      "branch": "feature/new-feature",
      "start_point": "main"
    }
  },
  "id": 8
}
```

### 9. **git_diff**
Muestra las diferencias entre commits o ramas.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `target` (string, opcional): Rama o commit a comparar
  - Default: `"HEAD~1"`
- `context_lines` (integer, opcional): Líneas de contexto
  - Default: 3

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_diff",
  "params": {
    "repo_path": "/path/to/repo",
    "target": "HEAD~1",
    "context_lines": 3
  },
  "id": 9
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "diff": "diff --git a/file.txt b/file.txt\nindex 1234567..abcdefg 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1,3 +1,4 @@\n line1\n line2\n+new line\n line3"
    }
  },
  "id": 9
}
```

### 10. **git_show**
Muestra el contenido de un commit específico.

**Parámetros:**
- `repo_path` (string, requerido): Ruta al repositorio Git
- `revision` (string, requerido): Hash del commit o nombre de rama

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "git_show",
  "params": {
    "repo_path": "/path/to/repo",
    "revision": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
  },
  "id": 10
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": {
      "commit": {
        "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
        "author": "User <user@example.com>",
        "date": "2024-01-15T10:30:00Z",
        "message": "Add new features and fix bugs",
        "changes": "diff --git a/file.txt b/file.txt\n..."
      }
    }
  },
  "id": 10
}
```

## 🔌 Integración con Chatbot

### Ejemplo de Uso
```python
from mcp_servers.mcp_client import MCPClient

# Inicializar cliente
client = MCPClient()

# Verificar estado del repositorio
status = await client.git_status("/path/to/repo")

# Agregar archivos
await client.git_add("/path/to/repo", ["file1.txt", "file2.txt"])

# Hacer commit
await client.git_commit("/path/to/repo", "Add new features")

# Ver historial
log = await client.git_log("/path/to/repo", max_count=5)
```

### Comandos del Chatbot
- `"git status"` - Ver estado del repositorio
- `"git add <files>"` - Agregar archivos al staging
- `"git commit <message>"` - Hacer commit
- `"git log"` - Ver historial de commits
- `"git branch"` - Listar ramas
- `"git checkout <branch>"` - Cambiar de rama
- `"git init"` - Inicializar repositorio

## 🔒 Seguridad

### Repositorios Permitidos
- **Configuración**: Se especifica al iniciar el servidor
- **Restricción**: Solo acceso a repositorios autorizados
- **Ejemplo**: `uvx mcp-server-git --repository /path/to/repo`

### Permisos
- **Lectura**: Solo repositorios autorizados
- **Escritura**: Solo en repositorios permitidos
- **Operaciones destructivas**: Confirmación requerida

## 🚨 Manejo de Errores

### Errores Comunes
- **Not a git repository**: Directorio no es un repositorio Git
- **Repository not found**: Repositorio no encontrado
- **Permission denied**: Sin permisos para la operación
- **Invalid branch**: Rama no existe
- **Merge conflicts**: Conflictos de merge

### Códigos de Error
- `-32600`: Invalid Request
- `-32601`: Method Not Found
- `-32602`: Invalid Params
- `-32603`: Internal Error
- `-32000`: Git Error

### Ejemplo de Error
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal Error",
    "data": {
      "error_type": "NOT_A_GIT_REPOSITORY",
      "error_message": "Directory '/path/to/dir' is not a git repository"
    }
  },
  "id": 1
}
```

## 📊 Límites y Restricciones

### Tamaño de Repositorio
- **Máximo**: 1GB por repositorio
- **Límite de archivos**: 10,000 archivos por operación
- **Timeout**: 60 segundos por operación

### Operaciones Concurrentes
- **Máximo**: 5 operaciones simultáneas
- **Rate limiting**: 50 operaciones por minuto
- **Queue**: Operaciones en cola si se excede el límite

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Repositorio permitido
export GIT_REPOSITORY_PATH="/path/to/repo"

# Tamaño máximo de repositorio
export GIT_MAX_REPO_SIZE=1073741824

# Timeout para operaciones
export GIT_TIMEOUT=60000
```

### Configuración del Servidor
```json
{
  "server": {
    "name": "git-mcp",
    "version": "1.0.0",
    "repository_path": "/path/to/repo",
    "max_repo_size": 1073741824,
    "timeout": 60000
  }
}
```

## 📚 Ejemplos de Uso

### Flujo Básico de Git
```bash
# Inicializar repositorio
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "git_init",
    "params": {
      "repo_path": "/path/to/new/repo"
    },
    "id": 1
  }'

# Ver estado
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "git_status",
    "params": {
      "repo_path": "/path/to/repo"
    },
    "id": 2
  }'
```

### Gestión de Ramas
```bash
# Crear rama
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "git_create_branch",
    "params": {
      "repo_path": "/path/to/repo",
      "branch_name": "feature/new-feature"
    },
    "id": 3
  }'
```

## 🌐 Compatibilidad

### Sistemas Operativos
- **Windows**: 10, 11
- **macOS**: 10.15+
- **Linux**: Ubuntu 18.04+, CentOS 7+

### Git
- **Versión mínima**: 2.20.0
- **Versión recomendada**: 2.40.0+
- **Versión LTS**: 2.39.x

### Python
- **Versión mínima**: 3.8.0
- **Versión recomendada**: 3.11.0+
- **Versión LTS**: 3.10.x

## 📝 Logs y Debugging

### Nivel de Log
- **INFO**: Operaciones normales
- **WARNING**: Advertencias no críticas
- **ERROR**: Errores que impiden el funcionamiento
- **DEBUG**: Información detallada para debugging

### Archivos de Log
- `git.log`: Log principal del servidor
- `operations.log`: Log de operaciones Git
- `errors.log`: Log de errores

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio oficial
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

MIT License - Desarrollado por Anthropic

## 🆘 Soporte

### Documentación Oficial
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Git Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
- [Anthropic MCP](https://docs.anthropic.com/en/docs/mcp)

### Contacto
- Issues en GitHub oficial
- Discord: #mcp-git
- Email: support@anthropic.com

---

**Desarrollado por Anthropic - Servidor MCP Oficial**
