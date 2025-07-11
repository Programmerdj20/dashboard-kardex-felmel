"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    @classmethod
    def _get_config_value(cls, key, default=None):
        """Obtener valor de configuración priorizando Streamlit secrets"""
        try:
            # Intentar obtener de Streamlit secrets primero
            return st.secrets.get(key, os.getenv(key, default))
        except Exception:
            # Si falla st.secrets, usar variables de entorno
            return os.getenv(key, default)
    
    # APIs - Priorizar Streamlit secrets, luego variables de entorno
    @property
    def OROCOLOMBIA_URL(self):
        return self._get_config_value('OROCOLOMBIA_URL')
    
    @property
    def OROCOLOMBIA_CONSUMER_KEY(self):
        return self._get_config_value('OROCOLOMBIA_CONSUMER_KEY')
    
    @property
    def OROCOLOMBIA_CONSUMER_SECRET(self):
        return self._get_config_value('OROCOLOMBIA_CONSUMER_SECRET')
    
    @property
    def GRUPOFELMEL_URL(self):
        return self._get_config_value('GRUPOFELMEL_URL')
    
    @property
    def GRUPOFELMEL_CONSUMER_KEY(self):
        return self._get_config_value('GRUPOFELMEL_CONSUMER_KEY')
    
    @property
    def GRUPOFELMEL_CONSUMER_SECRET(self):
        return self._get_config_value('GRUPOFELMEL_CONSUMER_SECRET')
    
    # Configuración general
    @property
    def PRODUCTS_PER_PAGE(self):
        return int(self._get_config_value('PRODUCTS_PER_PAGE', 100))
    
    @property
    def CACHE_DURATION_MINUTES(self):
        return int(self._get_config_value('CACHE_DURATION_MINUTES', 30))
    
    @property
    def DISCOUNT_PERCENTAGE(self):
        return int(self._get_config_value('DISCOUNT_PERCENTAGE', 35))
    
    # Rutas
    EXPORTS_DIR = 'exports'
    DATA_DIR = 'data'
    CACHE_DIR = 'data/cache'
    
    def validate(self):
        """Validar que todas las variables requeridas estén configuradas"""
        required_vars = [
            'OROCOLOMBIA_URL', 'OROCOLOMBIA_CONSUMER_KEY', 'OROCOLOMBIA_CONSUMER_SECRET',
            'GRUPOFELMEL_URL', 'GRUPOFELMEL_CONSUMER_KEY', 'GRUPOFELMEL_CONSUMER_SECRET'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(self, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
        
        return True