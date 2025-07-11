#!/usr/bin/env python3
"""
Script simple para ejecutar el dashboard sin configuración previa
"""
import subprocess
import sys
import os

def main():
    """Ejecutar el dashboard"""
    print("🚀 Iniciando Dashboard Kardex - Grupo Felmel...")
    
    # Cambiar al directorio correcto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado. Copiando desde .env.example...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("📝 Por favor edita el archivo .env con tus credenciales antes de continuar.")
            return
    
    # Crear directorios necesarios
    os.makedirs('data/cache', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    print("🌟 Iniciando aplicación...")
    print("🔗 La aplicación estará disponible en: http://localhost:8501")
    print("🛑 Para detener, presiona Ctrl+C")
    
    # Ejecutar streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "src/main.py",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard detenido por el usuario.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()