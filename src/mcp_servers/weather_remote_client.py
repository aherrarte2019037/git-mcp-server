#!/usr/bin/env python3
"""
Weather MCP Remote Client
Cliente para conectar al Weather MCP Server remoto en Railway
"""
import asyncio
import httpx
import json
import logging
from typing import Dict, Any

class WeatherRemoteClient:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        self.logger = logging.getLogger(__name__)
    
    async def _send_mcp_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enviar request MCP al servidor remoto"""
        try:
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            self.logger.info(f"Weather MCP JSON-RPC request: {json.dumps(request_data, indent=2)}")
            
            response = await self.client.post(
                f"{self.server_url}/mcp",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info(f"Weather MCP JSON-RPC response: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            self.logger.error(f"Weather MCP JSON-RPC error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud del servidor"""
        try:
            response = await self.client.get(f"{self.server_url}/health")
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Obtener clima actual"""
        return await self._send_mcp_request("tools/call", {
            "name": "get_weather",
            "arguments": {"city": city}
        })
    
    async def get_forecast(self, city: str, days: int = 3) -> Dict[str, Any]:
        """Obtener pronóstico del clima"""
        return await self._send_mcp_request("tools/call", {
            "name": "get_forecast",
            "arguments": {"city": city, "days": days}
        })
    
    async def get_weather_alerts(self, city: str) -> Dict[str, Any]:
        """Obtener alertas meteorológicas"""
        return await self._send_mcp_request("tools/call", {
            "name": "get_weather_alerts",
            "arguments": {"city": city}
        })
    
    async def close(self):
        """Cerrar conexiones"""
        await self.client.aclose()
