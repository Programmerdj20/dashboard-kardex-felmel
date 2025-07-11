#!/bin/bash

# Configuración para Hostinger
# Este script inicia la aplicación Streamlit

# Instalar dependencias si no están instaladas
pip install -r requirements.txt

# Crear directorio de logs si no existe
mkdir -p logs

# Iniciar aplicación Streamlit
streamlit run src/main.py --server.port 8000 --server.address 0.0.0.0 --server.headless true --server.runOnSave false --server.enableCORS false --server.enableXsrfProtection false