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
        
        # Define available operations
        self.available_operations = {
            "list": "Listar archivos en un directorio",
            "read": "Leer el contenido de un archivo",
            "write": "Crear o escribir en un archivo",
            "create_directory": "Crear un directorio"
        }
        
        # Define common unsupported operations and their suggestions
        self.unsupported_operations = {
            "modify": "modificar",
            "edit": "editar", 
            "update": "actualizar",
            "change": "cambiar",
            "delete": "eliminar",
            "remove": "remover",
            "move": "mover",
            "rename": "renombrar",
            "copy": "copiar",
            "create_directory": "crear directorio",
            "mkdir": "crear directorio",
            "rmdir": "eliminar directorio",
            "chmod": "cambiar permisos",
            "chown": "cambiar propietario",
            "find": "buscar archivos",
            "grep": "buscar texto",
            "search": "buscar"
        }
    
    def _detect_unsupported_operation(self, original_message: str) -> str:
        """Detect if user is requesting an unsupported filesystem operation"""
        message_lower = original_message.lower()
        
        # Check for unsupported operations with better pattern matching
        unsupported_patterns = [
            ("modifica", "modificar"),
            ("modificar", "modificar"),
            ("edita", "editar"),
            ("editar", "editar"),
            ("actualiza", "actualizar"),
            ("actualizar", "actualizar"),
            ("cambia", "cambiar"),
            ("cambiar", "cambiar"),
            ("elimina", "eliminar"),
            ("eliminar", "eliminar"),
            ("remueve", "remover"),
            ("remover", "remover"),
            ("borra", "eliminar"),
            ("borrar", "eliminar"),
            ("mueve", "mover"),
            ("mover", "mover"),
            ("renombra", "renombrar"),
            ("renombrar", "renombrar"),
            ("copia", "copiar"),
            ("copiar", "copiar"),
            ("duplica", "copiar"),
            ("duplicar", "copiar"),
            ("elimina directorio", "eliminar directorio"),
            ("eliminar directorio", "eliminar directorio"),
            ("rmdir", "eliminar directorio"),
            ("busca archivos", "buscar archivos"),
            ("buscar archivos", "buscar archivos"),
            ("busca texto", "buscar texto"),
            ("buscar texto", "buscar texto"),
            ("grep", "buscar texto"),
            ("find", "buscar archivos"),
            ("search", "buscar"),
            ("buscar", "buscar"),
            ("cambia permisos", "cambiar permisos"),
            ("chmod", "cambiar permisos"),
            ("cambia propietario", "cambiar propietario"),
            ("chown", "cambiar propietario")
        ]
        
        for pattern, description in unsupported_patterns:
            if pattern in message_lower:
                return f"❌ Lo siento, la operación de {description} no está disponible en este momento.\n\n" \
                       f"📋 **Operaciones disponibles:**\n" \
                       f"• `list files` o `ls` - Listar archivos\n" \
                       f"• `read file <ruta>` - Leer archivo\n" \
                       f"• `write file <ruta> <contenido>` - Crear/escribir archivo\n" \
                       f"• `create directory <ruta>` o `mkdir <ruta>` - Crear directorio\n\n" \
                       f"💡 **Sugerencia:** Para {description}, puedes usar las operaciones disponibles o " \
                       f"considerar usar comandos Git para versionado de archivos."
        
        return None
    
    async def execute_filesystem_intent(self, intent: Dict, original_message: str) -> str:
        """Execute filesystem intent based on detected action"""
        action = intent.get("action")
        path = intent.get("path", ".")
        content = intent.get("content", "")
        
        # Check if user is requesting an unsupported operation
        unsupported_msg = self._detect_unsupported_operation(original_message)
        if unsupported_msg:
            return unsupported_msg
        
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
        
        elif action == "create_directory":
            result = await self.mcp_client.filesystem_create_directory(path)
            if result["success"]:
                return f"📁 Directorio creado exitosamente: {path}"
            else:
                return f"❌ Error creando directorio: {result['error']}"
        
        elif action == "unsupported":
            operation = intent.get("operation", "operación no disponible")
            return f"❌ Lo siento, la operación de {operation} no está disponible en este momento.\n\n" \
                   f"📋 **Operaciones disponibles:**\n" \
                   f"• `list files` o `ls` - Listar archivos\n" \
                   f"• `read file <ruta>` - Leer archivo\n" \
                   f"• `write file <ruta> <contenido>` - Crear/escribir archivo\n" \
                   f"• `create directory <ruta>` o `mkdir <ruta>` - Crear directorio\n\n" \
                   f"💡 **Sugerencia:** Para {operation}, puedes usar las operaciones disponibles o " \
                   f"considerar usar comandos Git para versionado de archivos."
        
        return "❌ Acción no reconocida"
