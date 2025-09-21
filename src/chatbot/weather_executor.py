#!/usr/bin/env python3
"""
Weather MCP Executor
Ejecutor para comandos del Weather MCP Server remoto
"""
import logging
from typing import Dict, Any

class WeatherExecutor:
    def __init__(self, weather_client):
        self.weather_client = weather_client
        self.logger = logging.getLogger(__name__)
    
    async def execute_weather_intent(self, intent: Dict, original_message: str) -> str:
        """Ejecutar intent de clima basado en la acción detectada"""
        action = intent.get("action")
        city = intent.get("city", "Madrid")
        days = intent.get("days", 3)
        
        self.logger.info(f"Ejecutando acción de clima: {action} para ciudad: {city}")
        
        try:
            if action == "weather":
                result = await self.weather_client.get_weather(city)
                return self._format_weather_response(result)
            
            elif action == "forecast":
                result = await self.weather_client.get_forecast(city, days)
                return self._format_forecast_response(result)
            
            elif action == "alerts":
                result = await self.weather_client.get_weather_alerts(city)
                return self._format_alerts_response(result)
            
            else:
                return "❌ Acción de clima no reconocida"
                
        except Exception as e:
            self.logger.error(f"Error ejecutando acción de clima: {e}")
            return f"❌ Error obteniendo información del clima: {str(e)}"
    
    def _format_weather_response(self, result: Dict[str, Any]) -> str:
        """Formatear respuesta del clima actual"""
        if not result.get("success", False):
            return f"❌ Error: {result.get('error', 'Error desconocido')}"
        
        return f"""🌤️ **Clima en {result['city']}**

🌡️ **Temperatura:** {result['temperature']}°C
💧 **Humedad:** {result['humidity']}%
🔽 **Presión:** {result['pressure']} hPa
🌬️ **Viento:** {result['wind_speed']} km/h
☁️ **Descripción:** {result['description']}
⏰ **Actualizado:** {result['timestamp'][:19]}"""
    
    def _format_forecast_response(self, result: Dict[str, Any]) -> str:
        """Formatear respuesta del pronóstico"""
        if not result.get("success", False):
            return f"❌ Error: {result.get('error', 'Error desconocido')}"
        
        forecast_text = f"📅 **Pronóstico para {result['city']}**\n\n"
        
        for day in result['forecast']:
            forecast_text += f"📆 **{day['date']}**\n"
            forecast_text += f"   🌡️ {day['temperature']}°C\n"
            forecast_text += f"   💧 {day['humidity']}%\n"
            forecast_text += f"   ☁️ {day['description']}\n\n"
        
        return forecast_text
    
    def _format_alerts_response(self, result: Dict[str, Any]) -> str:
        """Formatear respuesta de alertas"""
        if not result.get("success", False):
            return f"❌ Error: {result.get('error', 'Error desconocido')}"
        
        if result['alert_count'] == 0:
            return f"✅ **No hay alertas meteorológicas para {result['city']}**"
        
        alerts_text = f"⚠️ **Alertas para {result['city']}**\n\n"
        
        for alert in result['alerts']:
            level_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴"}.get(alert['level'], "⚪")
            alerts_text += f"{level_emoji} **{alert['type'].replace('_', ' ').title()}**\n"
            alerts_text += f"   {alert['message']}\n\n"
        
        return alerts_text
