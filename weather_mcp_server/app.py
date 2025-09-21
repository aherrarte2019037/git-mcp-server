#!/usr/bin/env python3
"""
Weather MCP Server para Railway usando FastAPI
Servidor MCP remoto que proporciona información del clima
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Weather MCP Server",
    description="Servidor MCP remoto que proporciona información del clima",
    version="1.0.0"
)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY es requerida. Configúrala como variable de entorno.")
        
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def _get_weather_data(self, city: str) -> Dict[str, Any]:
        """Obtener datos del clima desde OpenWeatherMap"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Error HTTP al obtener clima: {e}")
            return {"error": f"Error al obtener datos del clima: {str(e)}"}
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return {"error": f"Error inesperado: {str(e)}"}
    
    async def _get_forecast_data(self, city: str, days: int = 3) -> Dict[str, Any]:
        """Obtener pronóstico del clima"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es",
                "cnt": days * 8  # 8 mediciones por día
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Error HTTP al obtener pronóstico: {e}")
            return {"error": f"Error al obtener pronóstico: {str(e)}"}
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return {"error": f"Error inesperado: {str(e)}"}
    
    async def close(self):
        """Cerrar conexiones"""
        await self.client.aclose()

# Instancia del servicio de clima
try:
    weather_service = WeatherService()
except ValueError as e:
    logger.error(f"Error de configuración: {e}")
    weather_service = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if weather_service is None:
        return {"status": "unhealthy", "service": "Weather MCP Server", "error": "OPENWEATHER_API_KEY not configured"}
    return {"status": "healthy", "service": "Weather MCP Server"}

@app.post("/mcp")
async def mcp_endpoint(request: Dict[str, Any]):
    """Endpoint principal MCP"""
    if weather_service is None:
        return {"error": "OPENWEATHER_API_KEY not configured. Please set the environment variable."}
    
    try:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "get_weather":
                city = arguments.get("city", "Madrid")
                return await get_weather(city)
            elif tool_name == "get_forecast":
                city = arguments.get("city", "Madrid")
                days = arguments.get("days", 3)
                return await get_forecast(city, days)
            elif tool_name == "get_weather_alerts":
                city = arguments.get("city", "Madrid")
                return await get_weather_alerts(city)
            else:
                return {"error": f"Tool '{tool_name}' not found"}
        
        return {"error": f"Method '{method}' not supported"}
        
    except Exception as e:
        logger.error(f"Error en endpoint MCP: {e}")
        return {"error": str(e)}

async def get_weather(city: str) -> Dict[str, Any]:
    """Obtener clima actual de una ciudad"""
    logger.info(f"Obteniendo clima para: {city}")
    
    data = await weather_service._get_weather_data(city)
    
    if "error" in data:
        return {
            "success": False,
            "error": data["error"]
        }
    
    try:
        weather_info = {
            "success": True,
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "main_weather": data["weather"][0]["main"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "timestamp": datetime.now().isoformat()
        }
        
        return weather_info
        
    except KeyError as e:
        logger.error(f"Error procesando datos del clima: {e}")
        return {
            "success": False,
            "error": f"Error procesando datos del clima: {str(e)}"
        }

async def get_forecast(city: str, days: int = 3) -> Dict[str, Any]:
    """Obtener pronóstico del clima para los próximos días"""
    logger.info(f"Obteniendo pronóstico para: {city}, {days} días")
    
    data = await weather_service._get_forecast_data(city, days)
    
    if "error" in data:
        return {
            "success": False,
            "error": data["error"]
        }
    
    try:
        forecast_list = []
        for item in data["list"][:days * 8:8]:  # Una medición por día
            forecast_list.append({
                "date": datetime.fromtimestamp(item["dt"] / 1000).strftime("%Y-%m-%d"),
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "description": item["weather"][0]["description"],
                "main_weather": item["weather"][0]["main"]
            })
        
        return {
            "success": True,
            "city": city,
            "forecast": forecast_list,
            "days": days,
            "timestamp": datetime.now().isoformat()
        }
        
    except KeyError as e:
        logger.error(f"Error procesando pronóstico: {e}")
        return {
            "success": False,
            "error": f"Error procesando pronóstico: {str(e)}"
        }

async def get_weather_alerts(city: str) -> Dict[str, Any]:
    """Obtener alertas meteorológicas para una ciudad"""
    logger.info(f"Obteniendo alertas para: {city}")
    
    # Simular alertas basadas en el clima actual
    weather_data = await weather_service._get_weather_data(city)
    
    if "error" in weather_data:
        return {
            "success": False,
            "error": weather_data["error"]
        }
    
    alerts = []
    
    try:
        temp = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]
        humidity = weather_data["main"]["humidity"]
        
        if temp > 35:
            alerts.append({
                "type": "heat_warning",
                "level": "high",
                "message": f"Temperatura alta: {temp}°C. Mantente hidratado."
            })
        elif temp < 0:
            alerts.append({
                "type": "cold_warning",
                "level": "medium",
                "message": f"Temperatura baja: {temp}°C. Abrígate bien."
            })
        
        if wind_speed > 15:
            alerts.append({
                "type": "wind_warning",
                "level": "medium",
                "message": f"Viento fuerte: {wind_speed} km/h. Ten cuidado al salir."
            })
        
        if humidity > 80:
            alerts.append({
                "type": "humidity_warning",
                "level": "low",
                "message": f"Alta humedad: {humidity}%. Puede sentirse bochornoso."
            })
        
        return {
            "success": True,
            "city": city,
            "alerts": alerts,
            "alert_count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    except KeyError as e:
        logger.error(f"Error procesando alertas: {e}")
        return {
            "success": False,
            "error": f"Error procesando alertas: {str(e)}"
        }

if __name__ == "__main__":
    if weather_service is None:
        print("❌ Error: OPENWEATHER_API_KEY no configurada")
        print("   Configura la variable de entorno OPENWEATHER_API_KEY")
        print("   Obtén una API key gratuita en: https://openweathermap.org/api")
        exit(1)
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌤️ Iniciando Weather MCP Server en {host}:{port}")
    print(f"🔑 API Key configurada: Sí")
    
    uvicorn.run(app, host=host, port=port)
