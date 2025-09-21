# Weather MCP Server para Railway

Servidor MCP remoto que proporciona información del clima usando FastMCP.

## 🌤️ Funcionalidades

- **get_weather(city)** - Clima actual de una ciudad

## 🚀 Deploy en Railway

### 1. Crear repositorio Git

```bash
git init
git add .
git commit -m "Weather MCP Server"
git remote add origin https://github.com/tu-usuario/weather-mcp-server.git
git push -u origin main
```

### 2. Conectar a Railway

1. Ve a [Railway.app](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Crea un nuevo proyecto
4. Conecta este repositorio

### 3. Deploy automático

Railway detectará automáticamente que es un proyecto Python y hará el deploy.

### 4. Obtener URL

Una vez deployado, Railway te dará una URL como:

```
https://weather-mcp-server-production.up.railway.app
```

## 🧪 Testing Local

```bash
pip install -r requirements.txt
python server.py
```

## 📡 Conectar desde tu Chatbot

```python
import httpx

async def get_weather(city: str, server_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{server_url}/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_weather",
                "arguments": {"city": city}
            }
        })
        return response.json()

# Uso
weather = await get_weather("Madrid", "https://tu-servidor.railway.app")
print(weather)
```

## 🔧 Configuración

- **Sin API key**: Usa datos de prueba (modo demo)
- **Con OPENWEATHER_API_KEY**: Usa datos reales de OpenWeatherMap

## 📊 Ejemplo de Respuesta

```json
{
  "success": true,
  "city": "Madrid",
  "temperature": 22.5,
  "humidity": 65,
  "description": "cielo despejado",
  "timestamp": "2025-09-21T10:30:00"
}
```
