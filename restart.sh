#!/bin/bash

# Script para reiniciar el Dashboard Kardex

echo "🔄 Reiniciando Dashboard Kardex..."

# Matar procesos existentes de streamlit
echo "🛑 Deteniendo procesos existentes..."
pkill -f "streamlit run" 2>/dev/null || true
sleep 2

# Verificar directorio
if [ ! -d "src" ]; then
    echo "❌ Error: No se encuentra el directorio 'src'. Asegúrate de estar en el directorio correcto."
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero: ./start.sh"
    exit 1
fi

source venv/bin/activate

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "📝 Por favor edita el archivo .env con tus credenciales."
fi

# Crear directorios necesarios
mkdir -p data/cache exports

echo "🚀 Iniciando Dashboard Kardex..."
echo "🔗 Dashboard disponible en:"
echo "   - Local: http://localhost:8501"
echo "   - Network: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "🛑 Para detener, presiona Ctrl+C o ejecuta: pkill -f 'streamlit run'"
echo ""

# Ejecutar Streamlit
streamlit run src/main.py --server.port 8501