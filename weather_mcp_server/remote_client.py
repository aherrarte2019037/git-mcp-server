#!/usr/bin/env python3
"""
Cliente MCP para conectar al Weather MCP Server remoto
"""
import asyncio
import json
import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WeatherRemoteClient:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _send_mcp_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enviar request MCP al servidor remoto"""
        try:
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            response = await self.client.post(
                f"{self.server_url}/mcp",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Error HTTP al conectar con servidor remoto: {e}")
            return {"success": False, "error": f"Error de conexión: {str(e)}"}
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return {"success": False, "error": f"Error inesperado: {str(e)}"}
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Obtener clima actual"""
        logger.info(f"Obteniendo clima para: {city}")
        return await self._send_mcp_request("tools/call", {
            "name": "get_weather",
            "arguments": {"city": city}
        })
    
    async def get_forecast(self, city: str, days: int = 3) -> Dict[str, Any]:
        """Obtener pronóstico del clima"""
        logger.info(f"Obteniendo pronóstico para: {city}, {days} días")
        return await self._send_mcp_request("tools/call", {
            "name": "get_forecast",
            "arguments": {"city": city, "days": days}
        })
    
    async def get_weather_alerts(self, city: str) -> Dict[str, Any]:
        """Obtener alertas meteorológicas"""
        logger.info(f"Obteniendo alertas para: {city}")
        return await self._send_mcp_request("tools/call", {
            "name": "get_weather_alerts",
            "arguments": {"city": city}
        })
    
    async def initialize(self) -> Dict[str, Any]:
        """Inicializar conexión MCP"""
        logger.info("Inicializando conexión MCP remota")
        return await self._send_mcp_request("initialize")
    
    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud del servidor"""
        try:
            response = await self.client.get(f"{self.server_url}/health")
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def close(self):
        """Cerrar conexión"""
        await self.client.aclose()

# Ejemplo de uso
async def test_remote_client():
    """Test del cliente remoto"""
    # URL del servidor (cambiar por la URL real de Railway)
    server_url = "https://tu-servidor.railway.app"
    
    client = WeatherRemoteClient(server_url)
    
    try:
        # Health check
        print("🔍 Verificando servidor...")
        health = await client.health_check()
        print(f"Health: {health}")
        
        # Inicializar
        print("🚀 Inicializando MCP...")
        init_result = await client.initialize()
        print(f"Init: {init_result}")
        
        # Test clima actual
        print("🌤️ Obteniendo clima...")
        weather = await client.get_weather("Madrid")
        print(f"Weather: {weather}")
        
        # Test pronóstico
        print("📅 Obteniendo pronóstico...")
        forecast = await client.get_forecast("Barcelona", 2)
        print(f"Forecast: {forecast}")
        
        # Test alertas
        print("⚠️ Obteniendo alertas...")
        alerts = await client.get_weather_alerts("Sevilla")
        print(f"Alerts: {alerts}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_remote_client())