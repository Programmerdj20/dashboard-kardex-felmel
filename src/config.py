"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # APIs
    OROCOLOMBIA_URL = os.getenv('OROCOLOMBIA_URL')
    OROCOLOMBIA_CONSUMER_KEY = os.getenv('OROCOLOMBIA_CONSUMER_KEY')
    OROCOLOMBIA_CONSUMER_SECRET = os.getenv('OROCOLOMBIA_CONSUMER_SECRET')
    
    GRUPOFELMEL_URL = os.getenv('GRUPOFELMEL_URL')
    GRUPOFELMEL_CONSUMER_KEY = os.getenv('GRUPOFELMEL_CONSUMER_KEY')
    GRUPOFELMEL_CONSUMER_SECRET = os.getenv('GRUPOFELMEL_CONSUMER_SECRET')
    
    # Configuración general
    PRODUCTS_PER_PAGE = int(os.getenv('PRODUCTS_PER_PAGE', 100))
    CACHE_DURATION_MINUTES = int(os.getenv('CACHE_DURATION_MINUTES', 30))
    DISCOUNT_PERCENTAGE = int(os.getenv('DISCOUNT_PERCENTAGE', 35))
    
    # Rutas
    EXPORTS_DIR = 'exports'
    DATA_DIR = 'data'
    CACHE_DIR = 'data/cache'
    
    @classmethod
    def validate(cls):
        """Validar que todas las variables requeridas estén configuradas"""
        required_vars = [
            'OROCOLOMBIA_URL', 'OROCOLOMBIA_CONSUMER_KEY', 'OROCOLOMBIA_CONSUMER_SECRET',
            'GRUPOFELMEL_URL', 'GRUPOFELMEL_CONSUMER_KEY', 'GRUPOFELMEL_CONSUMER_SECRET'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
        
        return True