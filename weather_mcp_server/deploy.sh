#!/bin/bash
# Script de deployment automático para Railway

echo "🌤️ Weather MCP Server - Deployment Script"
echo "=========================================="

# Verificar que estamos en la carpeta correcta
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py. Ejecuta este script desde la carpeta weather_mcp_server/"
    exit 1
fi

echo "✅ Archivos encontrados:"
ls -la app.py requirements.txt Procfile railway.json

echo ""
# Verificar que la API key esté configurada
if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "❌ Error: OPENWEATHER_API_KEY no configurada"
    echo "   Configura la variable de entorno:"
    echo "   export OPENWEATHER_API_KEY=tu_api_key_aqui"
    echo "   Obtén una API key gratuita en: https://openweathermap.org/api"
    exit 1
fi

echo "✅ API Key configurada: ${OPENWEATHER_API_KEY:0:8}..."

echo "🧪 Probando servidor localmente..."
python3 app.py &
SERVER_PID=$!

# Esperar a que el servidor inicie
sleep 3

# Probar health check
echo "🔍 Probando health check..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Health check exitoso"
else
    echo "❌ Health check falló"
    kill $SERVER_PID
    exit 1
fi

# Probar endpoint MCP
echo "🔍 Probando endpoint MCP..."
MCP_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"Madrid"}}}')

if echo "$MCP_RESPONSE" | grep -q "success.*true"; then
    echo "✅ Endpoint MCP funcionando"
else
    echo "❌ Endpoint MCP falló"
    echo "Respuesta: $MCP_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Detener servidor local
kill $SERVER_PID

echo ""
echo "🎉 ¡Servidor listo para desplegar en Railway!"
echo ""
echo "📋 Pasos siguientes:"
echo "1. Ve a https://railway.app"
echo "2. Crea un nuevo proyecto desde GitHub"
echo "3. Selecciona la carpeta weather_mcp_server/"
echo "4. Agrega la variable OPENWEATHER_API_KEY (opcional)"
echo "5. ¡Despliega!"
echo ""
echo "📖 Para más detalles, lee RAILWAY_DEPLOYMENT.md"
