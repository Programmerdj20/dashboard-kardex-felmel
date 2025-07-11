"""
Configuración específica para Streamlit Cloud
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno solo en desarrollo local
if not hasattr(st, 'secrets') or not st.secrets:
    load_dotenv()

def get_secret(key, default=None):
    """
    Obtener secreto de Streamlit Cloud o variable de entorno
    """
    try:
        # Intentar obtener de Streamlit secrets
        if hasattr(st, 'secrets') and st.secrets:
            return st.secrets.get(key, os.getenv(key, default))
        else:
            # Fallback a variables de entorno
            return os.getenv(key, default)
    except Exception:
        # Si todo falla, usar variables de entorno
        return os.getenv(key, default)

class StreamlitConfig:
    """Configuración optimizada para Streamlit Cloud"""
    
    def __init__(self):
        # APIs
        self.OROCOLOMBIA_URL = get_secret('OROCOLOMBIA_URL')
        self.OROCOLOMBIA_CONSUMER_KEY = get_secret('OROCOLOMBIA_CONSUMER_KEY')
        self.OROCOLOMBIA_CONSUMER_SECRET = get_secret('OROCOLOMBIA_CONSUMER_SECRET')
        
        self.GRUPOFELMEL_URL = get_secret('GRUPOFELMEL_URL')
        self.GRUPOFELMEL_CONSUMER_KEY = get_secret('GRUPOFELMEL_CONSUMER_KEY')
        self.GRUPOFELMEL_CONSUMER_SECRET = get_secret('GRUPOFELMEL_CONSUMER_SECRET')
        
        # Configuración general
        self.PRODUCTS_PER_PAGE = int(get_secret('PRODUCTS_PER_PAGE', 100))
        self.CACHE_DURATION_MINUTES = int(get_secret('CACHE_DURATION_MINUTES', 30))
        self.DISCOUNT_PERCENTAGE = int(get_secret('DISCOUNT_PERCENTAGE', 35))
        
        # Rutas
        self.EXPORTS_DIR = 'exports'
        self.DATA_DIR = 'data'
        self.CACHE_DIR = 'data/cache'
    
    def validate(self):
        """Validar que todas las variables requeridas estén configuradas"""
        required_vars = {
            'OROCOLOMBIA_URL': self.OROCOLOMBIA_URL,
            'OROCOLOMBIA_CONSUMER_KEY': self.OROCOLOMBIA_CONSUMER_KEY,
            'OROCOLOMBIA_CONSUMER_SECRET': self.OROCOLOMBIA_CONSUMER_SECRET,
            'GRUPOFELMEL_URL': self.GRUPOFELMEL_URL,
            'GRUPOFELMEL_CONSUMER_KEY': self.GRUPOFELMEL_CONSUMER_KEY,
            'GRUPOFELMEL_CONSUMER_SECRET': self.GRUPOFELMEL_CONSUMER_SECRET
        }
        
        missing = []
        for var_name, var_value in required_vars.items():
            if not var_value:
                missing.append(var_name)
        
        if missing:
            st.error(f"""
            **❌ Variables de entorno faltantes:**
            
            {', '.join(missing)}
            
            **Para configurar en Streamlit Cloud:**
            1. Ve a la configuración de tu app
            2. Sección "Secrets"
            3. Agrega estas variables:
            
            ```toml
            OROCOLOMBIA_URL = "https://orocolombia.co/wp-json/wc/v3/products"
            OROCOLOMBIA_CONSUMER_KEY = "tu_consumer_key"
            OROCOLOMBIA_CONSUMER_SECRET = "tu_consumer_secret"
            GRUPOFELMEL_URL = "https://app.grupofelmel.com/wp-json/wc/v3/products"
            GRUPOFELMEL_CONSUMER_KEY = "tu_consumer_key"
            GRUPOFELMEL_CONSUMER_SECRET = "tu_consumer_secret"
            ```
            """)
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
        
        return True