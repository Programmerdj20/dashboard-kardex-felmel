#!/bin/bash

# Script para detener el Dashboard Kardex

echo "🛑 Deteniendo Dashboard Kardex..."

# Matar procesos de streamlit
pkill -f "streamlit run" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Dashboard detenido exitosamente."
else
    echo "ℹ️  No hay procesos de Dashboard ejecutándose."
fi

# Verificar que se hayan detenido
sleep 1
RUNNING=$(ps aux | grep "streamlit run" | grep -v grep | wc -l)

if [ $RUNNING -eq 0 ]; then
    echo "✅ Todos los procesos han sido detenidos."
else
    echo "⚠️  Algunos procesos aún están ejecutándose. Forzando detención..."
    pkill -9 -f "streamlit run" 2>/dev/null
    echo "✅ Procesos terminados forzosamente."
fi