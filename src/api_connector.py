"""
Módulo para conectar con las APIs de WooCommerce
"""
import requests
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from streamlit_config import StreamlitConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WooCommerceAPI:
    """Clase para conectar con APIs de WooCommerce"""
    
    def __init__(self, url: str, consumer_key: str, consumer_secret: str, source_name: str):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.source_name = source_name
        self.session = requests.Session()
        self.config = StreamlitConfig()
        
        # Configurar autenticación
        self.session.auth = (consumer_key, consumer_secret)
        self.session.headers.update({
            'User-Agent': 'GrupoFelmel-Dashboard/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def get_products(self, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener productos de una página específica
        
        Args:
            page: Número de página
            per_page: Productos por página
            
        Returns:
            Lista de productos
        """
        params = {
            'page': page,
            'per_page': per_page,
            'orderby': 'modified',
            'order': 'desc',
            'status': 'publish'
        }
        
        try:
            # Log más simple para evitar spam en cloud
            if page == 1 or page % 5 == 0:  # Solo log cada 5 páginas
                logger.info(f"Consultando {self.source_name} página {page}...")
            
            response = self.session.get(self.url, params=params, timeout=30)
            response.raise_for_status()
            
            products = response.json()
            
            if page == 1 or page % 5 == 0:  # Solo log cada 5 páginas
                logger.info(f"{self.source_name} página {page}: {len(products)} productos")
            
            return products
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error consultando {self.source_name} página {page}: {str(e)}")
            logger.error(f"URL: {self.url}")
            logger.error(f"Response status: {response.status_code if 'response' in locals() else 'No response'}")
            raise
    
    def get_all_products(self, progress_callback=None, max_pages=None) -> List[Dict[str, Any]]:
        """
        Obtener todos los productos paginando automáticamente
        
        Args:
            progress_callback: Función para reportar progreso
            max_pages: Límite máximo de páginas (para evitar timeouts en cloud)
            
        Returns:
            Lista completa de productos
        """
        all_products = []
        page = 1
        consecutive_errors = 0
        max_consecutive_errors = 3
        
        # Límite de páginas para evitar timeouts en Streamlit Cloud
        if max_pages is None:
            max_pages = 50  # Límite por defecto para cloud
        
        while consecutive_errors < max_consecutive_errors and page <= max_pages:
            try:
                products = self.get_products(page=page, per_page=self.config.PRODUCTS_PER_PAGE)
                
                if not products:
                    logger.info(f"{self.source_name}: No hay más productos")
                    break
                
                all_products.extend(products)
                consecutive_errors = 0  # Reset counter
                
                # Callback para progreso
                if progress_callback:
                    progress_callback(self.source_name, page, len(all_products), len(products))
                
                # Si obtuvimos menos productos que el límite, es la última página
                if len(products) < self.config.PRODUCTS_PER_PAGE:
                    logger.info(f"{self.source_name}: Última página alcanzada")
                    break
                
                page += 1
                
                # Delay para evitar rate limiting
                delay = 1.0 if self.source_name == 'GrupoFelmel' else 0.5
                time.sleep(delay)
                
            except Exception as e:
                consecutive_errors += 1
                logger.warning(f"Error en {self.source_name} página {page} (intento {consecutive_errors}): {str(e)}")
                
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Demasiados errores en {self.source_name}. Usando datos parciales.")
                    break
                else:
                    # Esperar más tiempo antes del siguiente intento
                    time.sleep(consecutive_errors * 2)
        
        if page > max_pages:
            logger.warning(f"{self.source_name}: Alcanzado límite de {max_pages} páginas. Productos obtenidos: {len(all_products)}")
        
        logger.info(f"{self.source_name}: {len(all_products)} productos obtenidos")
        return all_products

class ProductManager:
    """Clase para gestionar productos de ambas APIs"""
    
    def __init__(self):
        self.config = StreamlitConfig()
        self.config.validate()
        
        self.orocolombia_api = WooCommerceAPI(
            url=self.config.OROCOLOMBIA_URL,
            consumer_key=self.config.OROCOLOMBIA_CONSUMER_KEY,
            consumer_secret=self.config.OROCOLOMBIA_CONSUMER_SECRET,
            source_name='OroColmbia'
        )
        
        self.grupofelmel_api = WooCommerceAPI(
            url=self.config.GRUPOFELMEL_URL,
            consumer_key=self.config.GRUPOFELMEL_CONSUMER_KEY,
            consumer_secret=self.config.GRUPOFELMEL_CONSUMER_SECRET,
            source_name='GrupoFelmel'
        )
    
    def process_product(self, product: Dict[str, Any], index: int) -> Dict[str, Any]:
        """
        Procesar un producto individual
        
        Args:
            product: Producto raw de la API
            index: Índice del producto
            
        Returns:
            Producto procesado
        """
        try:
            # Extraer precio
            price = 0
            if product.get('price'):
                price = float(product['price'])
            elif product.get('regular_price'):
                price = float(product['regular_price'])
            elif product.get('sale_price'):
                price = float(product['sale_price'])
            
            # Calcular precio con descuento
            config = StreamlitConfig()
            discount_price = price * (1 - config.DISCOUNT_PERCENTAGE / 100)
            
            # Extraer categorías
            categories = 'Sin categoría'
            if product.get('categories') and isinstance(product['categories'], list):
                categories = ', '.join([cat.get('name', '') for cat in product['categories']])
            
            # Extraer material de atributos
            material = 'N/A'
            if product.get('attributes') and isinstance(product['attributes'], list):
                for attr in product['attributes']:
                    name = attr.get('name', '').lower()
                    if any(term in name for term in ['material', 'composición', 'metal', 'tipo']):
                        if attr.get('options'):
                            material = ', '.join(attr['options'])
                            break
            
            # Si no hay material en atributos, buscar en descripción
            if material == 'N/A':
                description = (product.get('description', '') + product.get('short_description', '')).lower()
                if 'oro' in description:
                    material = 'Oro'
                elif 'plata' in description:
                    material = 'Plata'
                elif 'acero' in description:
                    material = 'Acero Inoxidable'
                elif 'titanio' in description:
                    material = 'Titanio'
            
            # Extraer stock
            stock = 0
            if product.get('stock_quantity') is not None:
                stock = int(product['stock_quantity'])
            
            # Fecha de modificación
            date_modified = datetime.now()
            if product.get('date_modified'):
                try:
                    date_modified = datetime.fromisoformat(product['date_modified'].replace('Z', '+00:00'))
                except:
                    pass
            
            # Imagen principal
            image_url = ''
            if product.get('images') and isinstance(product['images'], list) and len(product['images']) > 0:
                image_url = product['images'][0].get('src', '')
            
            # Validar que el SKU no sea None o vacío
            sku = product.get('sku', f'PROD-{index}')
            if not sku or sku == 'None':
                sku = f'PROD-{index}'
            
            # Validar que el name no sea None
            name = product.get('name', 'Sin nombre')
            if not name or name == 'None':
                name = 'Sin nombre'
            
            return {
                'id': product.get('id', f'temp_{index}'),
                'sku': str(sku),  # Asegurar que sea string
                'name': str(name),  # Asegurar que sea string
                'slug': product.get('slug', ''),
                'permalink': product.get('permalink', ''),
                'categories': categories,
                'material': material,
                'price': price,
                'discount_price': discount_price,
                'stock': stock,
                'status': product.get('status', 'draft'),
                'date_modified': date_modified,
                'image_url': image_url,
                'description': product.get('description', ''),
                'short_description': product.get('short_description', ''),
                'weight': product.get('weight', ''),
                'dimensions': product.get('dimensions', {}),
                'tags': ', '.join([tag.get('name', '') for tag in product.get('tags', [])]),
                'attributes': product.get('attributes', []),
                'variations': product.get('variations', []),
                'type': product.get('type', 'simple'),
                'featured': product.get('featured', False),
                'catalog_visibility': product.get('catalog_visibility', 'visible'),
                'raw_data': product  # Guardar datos originales por si acaso
            }
            
        except Exception as e:
            logger.error(f"Error procesando producto {index}: {str(e)}")
            return {
                'id': f'ERROR-{index}',
                'sku': f'ERROR-{index}',
                'name': 'Error al procesar',
                'slug': '',
                'permalink': '',
                'categories': 'Error',
                'material': 'Error',
                'price': 0,
                'discount_price': 0,
                'stock': 0,
                'status': 'draft',
                'date_modified': datetime.now(),
                'image_url': '',
                'description': '',
                'short_description': '',
                'weight': '',
                'dimensions': {},
                'tags': '',
                'attributes': [],
                'variations': [],
                'type': 'simple',
                'featured': False,
                'catalog_visibility': 'visible',
                'raw_data': {}
            }
    
    def fetch_all_products(self, progress_callback=None) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Obtener todos los productos de ambas APIs
        
        Args:
            progress_callback: Función para reportar progreso
            
        Returns:
            Tuple con DataFrames de (OroColmbia, GrupoFelmel)
        """
        logger.info("Iniciando consulta de productos...")
        
        # Detectar si estamos en Streamlit Cloud
        import streamlit as st
        is_cloud = hasattr(st, 'secrets') and st.secrets
        max_pages = 15 if is_cloud else None  # Límite más conservador en cloud
        
        logger.info(f"Ejecutando en {'Streamlit Cloud' if is_cloud else 'desarrollo local'}")
        
        # Obtener productos de OroColmbia
        logger.info("Obteniendo productos de OroColmbia...")
        orocolombia_products = self.orocolombia_api.get_all_products(progress_callback, max_pages)
        logger.info(f"Productos obtenidos de OroColmbia: {len(orocolombia_products)}")
        
        orocolombia_processed = [
            self.process_product(product, i) 
            for i, product in enumerate(orocolombia_products)
        ]
        logger.info(f"Productos procesados de OroColmbia: {len(orocolombia_processed)}")
        
        # Obtener productos de GrupoFelmel
        logger.info("Obteniendo productos de GrupoFelmel...")
        grupofelmel_products = self.grupofelmel_api.get_all_products(progress_callback, max_pages)
        logger.info(f"Productos obtenidos de GrupoFelmel: {len(grupofelmel_products)}")
        
        grupofelmel_processed = [
            self.process_product(product, i) 
            for i, product in enumerate(grupofelmel_products)
        ]
        logger.info(f"Productos procesados de GrupoFelmel: {len(grupofelmel_processed)}")
        
        # Convertir a DataFrames
        try:
            df_orocolombia = pd.DataFrame(orocolombia_processed)
            df_grupofelmel = pd.DataFrame(grupofelmel_processed)
            
            # Validar que los DataFrames no estén vacíos
            if df_orocolombia.empty:
                logger.warning("DataFrame de OroColmbia está vacío")
            if df_grupofelmel.empty:
                logger.warning("DataFrame de GrupoFelmel está vacío")
                
            logger.info(f"Productos procesados - OroColmbia: {len(df_orocolombia)}, GrupoFelmel: {len(df_grupofelmel)}")
            
            return df_orocolombia, df_grupofelmel
            
        except Exception as e:
            logger.error(f"Error creando DataFrames: {str(e)}")
            # Retornar DataFrames vacíos en caso de error
            return pd.DataFrame(), pd.DataFrame()
    
    def find_new_products(self, df_orocolombia: pd.DataFrame, df_grupofelmel: pd.DataFrame) -> pd.DataFrame:
        """
        Encontrar productos nuevos que están en OroColmbia pero no en GrupoFelmel
        y que tienen stock disponible
        
        Args:
            df_orocolombia: DataFrame de productos de OroColmbia
            df_grupofelmel: DataFrame de productos de GrupoFelmel
            
        Returns:
            DataFrame con productos nuevos
        """
        logger.info("Detectando productos nuevos...")
        
        try:
            # Validar que los DataFrames no estén vacíos
            if df_orocolombia.empty:
                logger.warning("DataFrame de OroColmbia está vacío")
                return pd.DataFrame()
            
            if df_grupofelmel.empty:
                logger.warning("DataFrame de GrupoFelmel está vacío - todos los productos serán considerados nuevos")
                grupofelmel_skus = set()
            else:
                # SKUs que están en GrupoFelmel (filtrar valores None)
                grupofelmel_skus = set(df_grupofelmel['sku'].dropna().unique())
            
            # Filtrar productos válidos de OroColmbia
            valid_orocolombia = df_orocolombia[
                (df_orocolombia['sku'].notna()) &  # SKU no debe ser None
                (df_orocolombia['sku'] != '') &
                (~df_orocolombia['sku'].str.startswith('PROD-')) &
                (~df_orocolombia['sku'].str.startswith('ERROR-')) &
                (df_orocolombia['price'] > 0) &
                (df_orocolombia['stock'] > 0)  # Solo productos con stock
            ].copy()
            
            # Productos nuevos: están en OroColmbia pero NO en GrupoFelmel
            new_products = valid_orocolombia[
                ~valid_orocolombia['sku'].isin(grupofelmel_skus)
            ].copy()
            
            logger.info(f"Productos nuevos encontrados: {len(new_products)}")
            
            if not new_products.empty:
                return new_products.sort_values('date_modified', ascending=False)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error en find_new_products: {str(e)}")
            return pd.DataFrame()