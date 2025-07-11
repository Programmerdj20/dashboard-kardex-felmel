#!/bin/bash

# Script de inicio para Dashboard Kardex - Grupo Felmel

echo "🚀 Iniciando Dashboard Kardex - Grupo Felmel..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Creando..."
    python -m venv venv
    echo "✅ Entorno virtual creado."
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar e instalar dependencias
echo "📦 Verificando dependencias..."
pip install streamlit requests python-dotenv pillow > /dev/null 2>&1

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "📝 Por favor edita el archivo .env con tus credenciales antes de continuar."
    echo "💡 Luego ejecuta este script nuevamente."
    exit 1
fi

# Crear directorios necesarios
mkdir -p data/cache exports

# Configurar Streamlit para evitar pregunta de email
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

echo "🌟 Iniciando aplicación..."
echo "🔗 La aplicación estará disponible en: http://localhost:8501"
echo "🛑 Para detener, presiona Ctrl+C"
echo ""

# Ejecutar Streamlit
streamlit run src/main.py --server.port 8501 --browser.gatherUsageStats false