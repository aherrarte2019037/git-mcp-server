#!/usr/bin/env python3
"""
Ejemplo SIMPLE de integración del Git Analyzer en un chatbot
Solo copia estos 3 archivos y usa este código
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_analyzer_client import GitAnalyzerClient
from git_analyzer_executor import GitAnalyzerExecutor

class ChatbotConGitAnalyzer:
    """Ejemplo SIMPLE de chatbot con Git Analyzer"""
    
    def __init__(self):
        self.git_analyzer_client = GitAnalyzerClient()
        self.git_analyzer_executor = GitAnalyzerExecutor(self.git_analyzer_client)
    
    async def inicializar(self):
        """Inicializar Git Analyzer"""
        print("🚀 Iniciando Git Analyzer...")
        success = await self.git_analyzer_client.start_analyzer_server()
        if success:
            print("✅ Git Analyzer iniciado!")
            return True
        else:
            print("❌ Error iniciando Git Analyzer")
            return False
    
    def detectar_comando_git_analyzer(self, mensaje: str):
        """Detectar comandos Git Analyzer"""
        mensaje_lower = mensaje.lower().strip()
        
        # Comandos fijos
        comandos = {
            "analyze repository": {"action": "analyze_repository", "repo_path": ".", "branch": "main", "depth": 100},
            "detect smells": {"action": "detect_smells", "repo_path": ".", "sensitivity_level": "medium"},
            "analyze contributors": {"action": "analyze_contributors", "repo_path": ".", "time_range": "1 year"},
            "get hotspots": {"action": "get_hotspots", "repo_path": ".", "threshold": 0.8}
        }
        
        # Comando fijo
        if mensaje_lower in comandos:
            return comandos[mensaje_lower]
        
        # Comando con parámetro
        if mensaje_lower.startswith("get code metrics "):
            archivo = mensaje[17:].strip()
            return {"action": "get_code_metrics", "file_path": archivo}
        
        return None
    
    async def procesar_mensaje(self, mensaje: str) -> str:
        """Procesar mensaje del usuario"""
        # Detectar comando Git Analyzer
        comando = self.detectar_comando_git_analyzer(mensaje)
        
        if comando:
            try:
                respuesta = await self.git_analyzer_executor.execute_git_analyzer_intent(comando, mensaje)
                return respuesta
            except Exception as e:
                return f"❌ Error: {e}"
        else:
            return f"🤖 Comando no reconocido: '{mensaje}'\n\nComandos disponibles:\n- analyze repository\n- get code metrics <archivo>\n- detect smells\n- analyze contributors\n- get hotspots"
    
    async def cerrar(self):
        """Cerrar conexiones"""
        await self.git_analyzer_client.close()

async def demo_automatico():
    """Demo automático"""
    print("🤖 Demo: Chatbot con Git Analyzer")
    print("=" * 40)
    
    chatbot = ChatbotConGitAnalyzer()
    
    if not await chatbot.inicializar():
        return
    
    # Comandos de prueba
    comandos = [
        "analyze repository",
        "get code metrics main.py",
        "detect smells",
        "analyze contributors",
        "get hotspots"
    ]
    
    for comando in comandos:
        print(f"\n👤 Usuario: {comando}")
        respuesta = await chatbot.procesar_mensaje(comando)
        print(f"🤖 Bot: {respuesta[:200]}..." if len(respuesta) > 200 else f"🤖 Bot: {respuesta}")
        print("-" * 40)
    
    await chatbot.cerrar()

async def demo_interactivo():
    """Demo interactivo"""
    print("🤖 Chatbot Interactivo con Git Analyzer")
    print("Escribe 'salir' para terminar")
    print("=" * 40)
    
    chatbot = ChatbotConGitAnalyzer()
    
    if not await chatbot.inicializar():
        return
    
    try:
        while True:
            mensaje = input("\n👤 Tú: ").strip()
            
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if mensaje:
                respuesta = await chatbot.procesar_mensaje(mensaje)
                print(f"🤖 Bot: {respuesta}")
    
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    
    finally:
        await chatbot.cerrar()

if __name__ == "__main__":
    print("Selecciona modo:")
    print("1. Demo automático")
    print("2. Demo interactivo")
    
    try:
        opcion = input("Opción (1 o 2): ").strip()
        
        if opcion == "1":
            asyncio.run(demo_automatico())
        elif opcion == "2":
            asyncio.run(demo_interactivo())
        else:
            print("Opción inválida, ejecutando demo automático...")
            asyncio.run(demo_automatico())
    
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
