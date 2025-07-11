"""
Utilidades para exportación de datos
"""
import pandas as pd
import io
from datetime import datetime
import streamlit as st

def export_products_to_csv(df_products, selected_skus=None, export_type="productos"):
    """
    Exportar productos a CSV
    
    Args:
        df_products: DataFrame con productos
        selected_skus: Lista de SKUs seleccionados (None = todos)
        export_type: Tipo de exportación ("productos" o "urls")
    
    Returns:
        Bytes del archivo CSV
    """
    # Filtrar productos seleccionados
    if selected_skus:
        df_export = df_products[df_products['sku'].isin(selected_skus)].copy()
    else:
        df_export = df_products.copy()
    
    if df_export.empty:
        return None
    
    if export_type == "productos":
        # Exportar datos completos de productos
        export_columns = [
            'sku', 'name', 'categories', 'material', 'price', 'discount_price', 
            'stock', 'status', 'date_modified', 'image_url', 'permalink'
        ]
        
        # Seleccionar solo las columnas que existen
        available_columns = [col for col in export_columns if col in df_export.columns]
        df_final = df_export[available_columns].copy()
        
        # Formatear datos para exportación
        if 'price' in df_final.columns:
            df_final['price'] = df_final['price'].round(2)
        if 'discount_price' in df_final.columns:
            df_final['discount_price'] = df_final['discount_price'].round(2)
        if 'date_modified' in df_final.columns:
            df_final['date_modified'] = df_final['date_modified'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Renombrar columnas para exportación
        column_names = {
            'sku': 'SKU',
            'name': 'Nombre',
            'categories': 'Categorías',
            'material': 'Material',
            'price': 'Precio',
            'discount_price': 'Precio con Descuento 35%',
            'stock': 'Stock',
            'status': 'Estado',
            'date_modified': 'Fecha Modificación',
            'image_url': 'URL Imagen',
            'permalink': 'Enlace Producto'
        }
        
        df_final = df_final.rename(columns=column_names)
        
    else:  # export_type == "urls"
        # Exportar solo URLs de imágenes
        df_final = df_export[['sku', 'name', 'image_url']].copy()
        df_final = df_final[df_final['image_url'].notna() & (df_final['image_url'] != '')].copy()
        
        # Renombrar columnas
        df_final = df_final.rename(columns={
            'sku': 'SKU',
            'name': 'Nombre Producto',
            'image_url': 'URL Imagen'
        })
    
    # Convertir a CSV
    output = io.StringIO()
    df_final.to_csv(output, index=False, encoding='utf-8-sig')
    
    return output.getvalue().encode('utf-8-sig')

def get_export_filename(export_type, selected_count=0):
    """
    Generar nombre de archivo para exportación
    
    Args:
        export_type: Tipo de exportación
        selected_count: Número de productos seleccionados
    
    Returns:
        Nombre del archivo
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if export_type == "productos":
        if selected_count > 0:
            return f"productos_seleccionados_{selected_count}_{timestamp}.csv"
        else:
            return f"productos_todos_{timestamp}.csv"
    else:  # urls
        if selected_count > 0:
            return f"urls_imagenes_seleccionadas_{selected_count}_{timestamp}.csv"
        else:
            return f"urls_imagenes_todas_{timestamp}.csv"

def create_download_button(df_products, selected_skus, export_type, button_text, button_key):
    """
    Crear botón de descarga con el archivo CSV
    
    Args:
        df_products: DataFrame con productos
        selected_skus: SKUs seleccionados
        export_type: Tipo de exportación
        button_text: Texto del botón
        button_key: Key única del botón
    
    Returns:
        True si se creó el botón, False si no hay datos
    """
    if df_products.empty:
        return False
    
    # Filtrar productos si hay selección
    if selected_skus:
        export_data = df_products[df_products['sku'].isin(selected_skus)]
        selected_count = len(selected_skus)  # Contar los SKUs seleccionados reales
    else:
        export_data = df_products
        selected_count = 0
    
    if export_data.empty:
        st.warning("⚠️ No hay productos para exportar")
        return False
    
    # Generar CSV
    csv_data = export_products_to_csv(df_products, selected_skus, export_type)
    
    if csv_data is None:
        st.error("❌ Error al generar el archivo CSV")
        return False
    
    # Generar nombre de archivo
    filename = get_export_filename(export_type, selected_count)
    
    # Crear botón de descarga
    st.download_button(
        label=button_text,
        data=csv_data,
        file_name=filename,
        mime='text/csv',
        key=button_key,
        use_container_width=True
    )
    
    return True

def show_export_summary(df_products, selected_skus):
    """
    Mostrar resumen de lo que se va a exportar
    
    Args:
        df_products: DataFrame con productos
        selected_skus: SKUs seleccionados
    """
    if selected_skus:
        export_data = df_products[df_products['sku'].isin(selected_skus)]
        st.info(f"📊 Se exportarán **{len(export_data)}** productos seleccionados")
    else:
        st.info(f"📊 Se exportarán **{len(df_products)}** productos totales")
    
    # Mostrar productos con imágenes
    if not df_products.empty:
        products_with_images = df_products[
            df_products['image_url'].notna() & 
            (df_products['image_url'] != '')
        ]
        
        if selected_skus:
            selected_with_images = products_with_images[
                products_with_images['sku'].isin(selected_skus)
            ]
            st.info(f"🖼️ **{len(selected_with_images)}** productos seleccionados tienen imágenes")
        else:
            st.info(f"🖼️ **{len(products_with_images)}** productos totales tienen imágenes")