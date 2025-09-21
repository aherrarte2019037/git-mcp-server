# 🌤️ Weather MCP Server

## 📋 Descripción

Servidor MCP (Model Context Protocol) remoto especializado en consultas meteorológicas. Proporciona información del clima actual, pronósticos y alertas meteorológicas utilizando la API de OpenWeatherMap.

## 🚀 Características

- **Clima actual**: Temperatura, humedad, condiciones actuales
- **Pronósticos**: Predicciones para múltiples días
- **Alertas meteorológicas**: Avisos de condiciones peligrosas
- **Despliegue en la nube**: Servidor remoto en Railway
- **API RESTful**: Endpoints HTTP estándar
- **Autenticación**: API Key requerida para OpenWeatherMap

## 🛠️ Instalación

### Requisitos
- Python 3.8+
- API Key de OpenWeatherMap
- Cuenta en Railway (para despliegue)

### Instalación Local
```bash
# Clonar el repositorio
git clone <repository-url>
cd weather_mcp_server

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key
export OPENWEATHER_API_KEY="tu_api_key_aqui"

# Ejecutar servidor local
python app.py
```

### Despliegue en Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login en Railway
railway login

# Desplegar
railway up
```

## 📡 Especificación del Servidor

### **Transporte**: HTTP/HTTPS
### **Protocolo**: JSON-RPC 2.0 sobre HTTP
### **Puerto**: 8000 (local), 443 (Railway)
### **URL**: `https://git-mcp-server-production-a0cf.up.railway.app`

## 🔧 Endpoints Disponibles

### 1. **Health Check**
Verifica el estado del servidor.

**Endpoint**: `GET /health`

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Weather MCP Server",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. **MCP Endpoint**
Endpoint principal para todas las operaciones MCP.

**Endpoint**: `POST /mcp`

**Headers:**
```
Content-Type: application/json
```

## 🌤️ Herramientas Disponibles

### 1. **get_weather**
Obtiene el clima actual de una ciudad.

**Parámetros:**
- `city` (string, requerido): Nombre de la ciudad
- `units` (string, opcional): Unidades de temperatura
  - Valores: `"metric"`, `"imperial"`, `"kelvin"`
  - Default: `"metric"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "get_weather",
  "params": {
    "city": "Madrid",
    "units": "metric"
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
      "city": "Madrid",
      "temperature": 19.12,
      "humidity": 65,
      "description": "clear sky",
      "wind_speed": 3.6,
      "pressure": 1013,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  },
  "id": 1
}
```

### 2. **get_forecast**
Obtiene el pronóstico del clima para múltiples días.

**Parámetros:**
- `city` (string, requerido): Nombre de la ciudad
- `days` (integer, opcional): Número de días (1-5)
  - Default: 3
- `units` (string, opcional): Unidades de temperatura
  - Default: `"metric"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "get_forecast",
  "params": {
    "city": "Paris",
    "days": 3,
    "units": "metric"
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
      "city": "Paris",
      "forecast": [
        {
          "date": "2024-01-15",
          "temperature": 15.2,
          "humidity": 70,
          "description": "partly cloudy",
          "wind_speed": 4.1
        },
        {
          "date": "2024-01-16",
          "temperature": 17.8,
          "humidity": 68,
          "description": "clear sky",
          "wind_speed": 3.2
        }
      ]
    }
  },
  "id": 2
}
```

### 3. **get_weather_alerts**
Obtiene alertas meteorológicas para una ciudad.

**Parámetros:**
- `city` (string, requerido): Nombre de la ciudad
- `country` (string, opcional): Código de país (ISO 3166-1 alpha-2)
  - Default: `"US"`

**Ejemplo de Petición:**
```json
{
  "jsonrpc": "2.0",
  "method": "get_weather_alerts",
  "params": {
    "city": "New York",
    "country": "US"
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
      "city": "New York",
      "country": "US",
      "alert_count": 0,
      "alerts": []
    }
  },
  "id": 3
}
```

## 🔌 Integración con Chatbot

### Ejemplo de Uso
```python
from mcp_servers.weather_remote_client import WeatherRemoteClient

# Inicializar cliente
client = WeatherRemoteClient("https://git-mcp-server-production-a0cf.up.railway.app")

# Verificar salud del servidor
health = await client.health_check()

# Obtener clima actual
weather = await client.get_weather("Madrid")

# Obtener pronóstico
forecast = await client.get_forecast("Paris", 3)

# Obtener alertas
alerts = await client.get_weather_alerts("New York")
```

### Comandos del Chatbot
- `"weather in <city>"` - Clima actual
- `"clima en <city>"` - Clima actual (español)
- `"forecast in <city>"` - Pronóstico
- `"pronóstico en <city>"` - Pronóstico (español)
- `"weather alerts in <city>"` - Alertas meteorológicas
- `"alertas en <city>"` - Alertas (español)

## 🔑 Configuración

### Variables de Entorno
```bash
# API Key de OpenWeatherMap (REQUERIDA)
export OPENWEATHER_API_KEY="tu_api_key_aqui"

# Puerto del servidor
export PORT=8000

# Host del servidor
export HOST=0.0.0.0
```

### Obtener API Key
1. Visitar [OpenWeatherMap](https://openweathermap.org/api)
2. Crear cuenta gratuita
3. Generar API Key
4. Configurar variable de entorno

## 📊 Códigos de Respuesta

### HTTP Status Codes
- **200 OK**: Petición exitosa
- **400 Bad Request**: Parámetros inválidos
- **401 Unauthorized**: API Key inválida
- **404 Not Found**: Ciudad no encontrada
- **429 Too Many Requests**: Límite de API excedido
- **500 Internal Server Error**: Error del servidor

### Códigos de Error JSON-RPC
- `-32600`: Invalid Request
- `-32601`: Method Not Found
- `-32602`: Invalid Params
- `-32603`: Internal Error
- `-32000`: Server Error

## 🚨 Manejo de Errores

### Errores Comunes
- **API Key no configurada**: `OPENWEATHER_API_KEY` requerida
- **Ciudad no encontrada**: Nombre de ciudad inválido
- **Límite de API excedido**: Demasiadas peticiones
- **Servicio no disponible**: OpenWeatherMap temporalmente fuera de servicio

### Ejemplo de Error
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal Error",
    "data": {
      "error_type": "API_ERROR",
      "error_message": "City not found"
    }
  },
  "id": 1
}
```

## 📝 Logs y Debugging

### Nivel de Log
- **INFO**: Operaciones normales
- **WARNING**: Advertencias no críticas
- **ERROR**: Errores que impiden el funcionamiento
- **DEBUG**: Información detallada para debugging

### Archivos de Log
- `weather_server.log`: Log principal del servidor
- `api_calls.log`: Log de llamadas a OpenWeatherMap
- `errors.log`: Log de errores

## 🔧 Configuración Avanzada

### Timeouts
```python
# Timeout para llamadas a OpenWeatherMap
OPENWEATHER_TIMEOUT = 10.0

# Timeout para respuestas del servidor
SERVER_TIMEOUT = 30.0
```

### Rate Limiting
```python
# Límite de peticiones por minuto
RATE_LIMIT = 60

# Límite de peticiones por día
DAILY_LIMIT = 1000
```

## 📚 Ejemplos de Uso

### Clima Actual
```bash
curl -X POST https://git-mcp-server-production-a0cf.up.railway.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get_weather",
    "params": {
      "city": "Madrid",
      "units": "metric"
    },
    "id": 1
  }'
```

### Pronóstico
```bash
curl -X POST https://git-mcp-server-production-a0cf.up.railway.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get_forecast",
    "params": {
      "city": "Paris",
      "days": 3
    },
    "id": 2
  }'
```

### Health Check
```bash
curl -X GET https://git-mcp-server-production-a0cf.up.railway.app/health
```

## 🌍 Ciudades Soportadas

### Formato de Búsqueda
- **Nombre de ciudad**: "Madrid", "Paris", "New York"
- **Ciudad, País**: "Madrid, ES", "Paris, FR"
- **Coordenadas**: "40.4168, -3.7038" (lat, lon)
- **Código postal**: "28001" (con código de país)

### Ejemplos
- `"Madrid"` → Madrid, España
- `"Madrid, ES"` → Madrid, España
- `"New York, US"` → Nueva York, Estados Unidos
- `"London, GB"` → Londres, Reino Unido

## 📊 Métricas y Monitoreo

### Métricas Disponibles
- **Peticiones por minuto**: Rate de uso
- **Tiempo de respuesta**: Latencia promedio
- **Tasa de error**: Porcentaje de errores
- **Uso de API**: Llamadas a OpenWeatherMap

### Endpoints de Monitoreo
- `GET /health` - Estado del servidor
- `GET /metrics` - Métricas de rendimiento
- `GET /status` - Estado detallado

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
- Discord: #weather-mcp

---

**Desarrollado para el curso CC3067 Redes - Universidad del Valle de Guatemala**
