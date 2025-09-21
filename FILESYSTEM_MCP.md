# 📁 Filesystem MCP Server

## 📋 Descripción

Servidor MCP (Model Context Protocol) oficial de Anthropic para operaciones del sistema de archivos. Permite leer, escribir, listar y gestionar archivos y directorios de forma segura desde aplicaciones de IA.

## 🚀 Características

- **Operaciones básicas**: Leer, escribir, listar archivos
- **Gestión de directorios**: Crear, eliminar, navegar directorios
- **Seguridad**: Acceso controlado a rutas permitidas
- **Estándar oficial**: Desarrollado por Anthropic
- **Alto rendimiento**: Optimizado para operaciones de archivos
- **Multiplataforma**: Compatible con Windows, macOS, Linux

## 🛠️ Instalación

### Requisitos
- Node.js 16+
- npm o yarn

### Instalación
```bash
# Instalar globalmente
npm install -g @modelcontextprotocol/server-filesystem

# O usar con npx
npx @modelcontextprotocol/server-filesystem
```

### Configuración con Claude Desktop
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
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

### 1. **read_file**
Lee el contenido de un archivo.

**Parámetros:**
- `path` (string, requerido): Ruta al archivo a leer

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "read_file",
  "params": {
    "path": "/path/to/file.txt"
  },
  "id": 1
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": "Contenido del archivo...",
    "size": 1024,
    "last_modified": "2024-01-15T10:30:00Z"
  },
  "id": 1
}
```

### 2. **write_file**
Escribe contenido a un archivo.

**Parámetros:**
- `path` (string, requerido): Ruta al archivo a escribir
- `content` (string, requerido): Contenido a escribir
- `mode` (string, opcional): Modo de escritura
  - Valores: `"overwrite"`, `"append"`
  - Default: `"overwrite"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "write_file",
  "params": {
    "path": "/path/to/file.txt",
    "content": "Nuevo contenido del archivo",
    "mode": "overwrite"
  },
  "id": 2
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "path": "/path/to/file.txt",
    "size": 1024
  },
  "id": 2
}
```

### 3. **list_directory**
Lista el contenido de un directorio.

**Parámetros:**
- `path` (string, requerido): Ruta al directorio a listar
- `recursive` (boolean, opcional): Listar recursivamente
  - Default: `false`
- `include_hidden` (boolean, opcional): Incluir archivos ocultos
  - Default: `false`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "list_directory",
  "params": {
    "path": "/path/to/directory",
    "recursive": false,
    "include_hidden": false
  },
  "id": 3
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "path": "/path/to/directory",
    "items": [
      {
        "name": "file1.txt",
        "type": "file",
        "size": 1024,
        "last_modified": "2024-01-15T10:30:00Z"
      },
      {
        "name": "subdirectory",
        "type": "directory",
        "size": null,
        "last_modified": "2024-01-15T10:30:00Z"
      }
    ]
  },
  "id": 3
}
```

### 4. **create_directory**
Crea un nuevo directorio.

**Parámetros:**
- `path` (string, requerido): Ruta del directorio a crear
- `recursive` (boolean, opcional): Crear directorios padre si no existen
  - Default: `true`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "create_directory",
  "params": {
    "path": "/path/to/new/directory",
    "recursive": true
  },
  "id": 4
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "path": "/path/to/new/directory"
  },
  "id": 4
}
```

### 5. **delete_file**
Elimina un archivo.

**Parámetros:**
- `path` (string, requerido): Ruta del archivo a eliminar

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "delete_file",
  "params": {
    "path": "/path/to/file.txt"
  },
  "id": 5
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "path": "/path/to/file.txt"
  },
  "id": 5
}
```

### 6. **delete_directory**
Elimina un directorio.

**Parámetros:**
- `path` (string, requerido): Ruta del directorio a eliminar
- `recursive` (boolean, opcional): Eliminar recursivamente
  - Default: `false`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "delete_directory",
  "params": {
    "path": "/path/to/directory",
    "recursive": true
  },
  "id": 6
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "path": "/path/to/directory"
  },
  "id": 6
}
```

### 7. **move_file**
Mueve o renombra un archivo.

**Parámetros:**
- `source` (string, requerido): Ruta de origen
- `destination` (string, requerido): Ruta de destino

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "move_file",
  "params": {
    "source": "/path/to/old_file.txt",
    "destination": "/path/to/new_file.txt"
  },
  "id": 7
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "source": "/path/to/old_file.txt",
    "destination": "/path/to/new_file.txt"
  },
  "id": 7
}
```

### 8. **get_file_info**
Obtiene información detallada de un archivo.

**Parámetros:**
- `path` (string, requerido): Ruta del archivo

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "get_file_info",
  "params": {
    "path": "/path/to/file.txt"
  },
  "id": 8
}
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "path": "/path/to/file.txt",
    "type": "file",
    "size": 1024,
    "created": "2024-01-15T10:30:00Z",
    "modified": "2024-01-15T10:30:00Z",
    "permissions": "rw-r--r--",
    "owner": "user",
    "group": "group"
  },
  "id": 8
}
```

## 🔌 Integración con Chatbot

### Ejemplo de Uso
```python
from mcp_servers.mcp_client import MCPClient

# Inicializar cliente
client = MCPClient()

# Leer archivo
content = await client.read_file("/path/to/file.txt")

# Escribir archivo
await client.write_file("/path/to/new_file.txt", "Contenido")

# Listar directorio
items = await client.list_directory("/path/to/directory")
```

### Comandos del Chatbot
- `"list files"` - Listar archivos en directorio actual
- `"ls"` - Listar archivos (comando corto)
- `"read file <path>"` - Leer archivo específico
- `"write file <path> <content>"` - Escribir archivo
- `"create directory <path>"` - Crear directorio
- `"delete file <path>"` - Eliminar archivo

## 🔒 Seguridad

### Rutas Permitidas
- **Configuración**: Se especifica al iniciar el servidor
- **Restricción**: Solo acceso a directorios autorizados
- **Ejemplo**: `npx @modelcontextprotocol/server-filesystem /allowed/path`

### Permisos
- **Lectura**: Solo archivos en rutas permitidas
- **Escritura**: Solo en directorios autorizados
- **Eliminación**: Confirmación requerida para operaciones destructivas

## 🚨 Manejo de Errores

### Errores Comunes
- **File not found**: Archivo no encontrado
- **Permission denied**: Sin permisos para la operación
- **Path not allowed**: Ruta fuera del directorio permitido
- **Directory not empty**: Directorio no vacío para eliminación

### Códigos de Error
- `-32600`: Invalid Request
- `-32601`: Method Not Found
- `-32602`: Invalid Params
- `-32603`: Internal Error
- `-32000`: File System Error

### Ejemplo de Error
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal Error",
    "data": {
      "error_type": "FILE_NOT_FOUND",
      "error_message": "File '/path/to/file.txt' not found"
    }
  },
  "id": 1
}
```

## 📊 Límites y Restricciones

### Tamaño de Archivo
- **Máximo**: 10MB por archivo
- **Límite de memoria**: 100MB para operaciones en memoria
- **Timeout**: 30 segundos por operación

### Operaciones Concurrentes
- **Máximo**: 10 operaciones simultáneas
- **Rate limiting**: 100 operaciones por minuto
- **Queue**: Operaciones en cola si se excede el límite

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Directorio permitido
export FILESYSTEM_ALLOWED_PATH="/path/to/allowed/directory"

# Tamaño máximo de archivo
export FILESYSTEM_MAX_FILE_SIZE=10485760

# Timeout para operaciones
export FILESYSTEM_TIMEOUT=30000
```

### Configuración del Servidor
```json
{
  "server": {
    "name": "filesystem-mcp",
    "version": "1.0.0",
    "allowed_paths": ["/path/to/allowed/directory"],
    "max_file_size": 10485760,
    "timeout": 30000
  }
}
```

## 📚 Ejemplos de Uso

### Operaciones Básicas
```bash
# Leer archivo
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "read_file",
    "params": {
      "path": "/path/to/file.txt"
    },
    "id": 1
  }'

# Escribir archivo
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "write_file",
    "params": {
      "path": "/path/to/new_file.txt",
      "content": "Nuevo contenido"
    },
    "id": 2
  }'
```

### Gestión de Directorios
```bash
# Listar directorio
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "list_directory",
    "params": {
      "path": "/path/to/directory"
    },
    "id": 3
  }'
```

## 🌐 Compatibilidad

### Sistemas Operativos
- **Windows**: 10, 11
- **macOS**: 10.15+
- **Linux**: Ubuntu 18.04+, CentOS 7+

### Node.js
- **Versión mínima**: 16.0.0
- **Versión recomendada**: 18.0.0+
- **Versión LTS**: 20.x

## 📝 Logs y Debugging

### Nivel de Log
- **INFO**: Operaciones normales
- **WARNING**: Advertencias no críticas
- **ERROR**: Errores que impiden el funcionamiento
- **DEBUG**: Información detallada para debugging

### Archivos de Log
- `filesystem.log`: Log principal del servidor
- `operations.log`: Log de operaciones de archivos
- `errors.log`: Log de errores

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio oficial
2. Crear rama para feature
3. Implementar cambios
4. Agregar tests
5. Crear pull request

### Estándares de Código
- ESLint para JavaScript
- JSDoc para documentación
- Tests para nuevas funcionalidades
- Documentación actualizada

## 📄 Licencia

MIT License - Desarrollado por Anthropic

## 🆘 Soporte

### Documentación Oficial
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Anthropic MCP](https://docs.anthropic.com/en/docs/mcp)

### Contacto
- Issues en GitHub oficial
- Discord: #mcp-filesystem
- Email: support@anthropic.com

---

**Desarrollado por Anthropic - Servidor MCP Oficial**
