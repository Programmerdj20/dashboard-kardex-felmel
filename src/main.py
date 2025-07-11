"""
Dashboard principal de Grupo Felmel
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os
import sys
import base64
from PIL import Image, ImageDraw
import io

# Añadir src al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_connector import ProductManager
from config import Config
from export_utils import create_download_button, show_export_summary

# Rutas de logos
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Logo_circulo_512.webp")
favicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Logo_circulo_256.webp")

# Configuración de la página
st.set_page_config(
    page_title="Kardex - Grupo Felmel",
    page_icon=favicon_path if os.path.exists(favicon_path) else "🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores Felmel
COLORS = {
    'primary': '#021A23',      # Azul oscuro principal
    'secondary': '#E7F1F2',    # Blanco grisáceo
    'accent': '#7B9E7E',       # Verde suave
    'text_light': '#E7F1F2',
    'text_dark': '#021A23',
    'background_dark': '#021A23',
    'background_light': '#E7F1F2',
    'border': '#7B9E7E'
}

@st.cache_data
def get_logo_base64(logo_path):
    """Convertir logo a base64 para uso en CSS"""
    try:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                img_bytes = f.read()
            img_str = base64.b64encode(img_bytes).decode()
            return f"data:image/webp;base64,{img_str}"
        return None
    except Exception as e:
        st.error(f"Error procesando logo: {e}")
        return None

# Estilos CSS personalizados con paleta Felmel
st.markdown("""
<style>
    /* Header principal con paleta Felmel */
    .main-header {
        background: linear-gradient(135deg, #021A23 0%, #7B9E7E 50%, #E7F1F2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: #E7F1F2;
        box-shadow: 0 8px 32px rgba(2, 26, 35, 0.6);
        border: 1px solid #7B9E7E;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        color: #021A23;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.85;
        color: #021A23;
    }
    
    /* Mejorar las métricas con paleta Felmel */
    .stMetric {
        background: #E7F1F2;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #7B9E7E;
    }
    
    /* FORZAR TODO EL TEXTO DE LAS MÉTRICAS A COLOR OSCURO */
    .stMetric * {
        color: #021A23 !important;
    }
    
    /* Badge para productos nuevos */
    .new-product-badge {
        background: linear-gradient(45deg, #7B9E7E, #E7F1F2);
        color: #021A23;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(123, 158, 126, 0.3);
    }
    
    /* Mejorar tablas */
    .stDataFrame {
        border: 1px solid #7B9E7E;
        border-radius: 10px;
        background: #E7F1F2;
    }
    
    /* Mensajes de éxito */
    .success-message {
        background: linear-gradient(135deg, #7B9E7E, #E7F1F2);
        border: 1px solid #7B9E7E;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #021A23;
        box-shadow: 0 4px 16px rgba(123, 158, 126, 0.2);
    }
    
    /* Mensajes de error */
    .error-message {
        background: linear-gradient(135deg, #021A23, #7B9E7E);
        border: 1px solid #ff6b6b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #E7F1F2;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.2);
    }
    
    /* Mejorar sidebar */
    .css-1d391kg {
        background: #021A23;
    }
    
    /* Botones mejorados con mejor legibilidad */
    .stButton > button {
        background: #7B9E7E;
        color: #021A23 !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #E7F1F2;
        color: #021A23 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(123, 158, 126, 0.4);
    }
    
    /* Ocultar elementos no profesionales */
    .stDeployButton {
        display: none;
    }
    
    /* Mejorar contraste en inputs con paleta Felmel */
    .stTextInput > div > div > input {
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
        color: #021A23 !important;
        caret-color: #021A23 !important;
        cursor: text !important;
    }
    
    .stSelectbox > div > div > select {
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
        color: #021A23 !important;
    }
    
    .stNumberInput > div > div > input {
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
        color: #021A23 !important;
    }
    
    .stNumberInput input {
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
        color: #021A23 !important;
    }
    
    .stNumberInput div[data-baseweb="input"] {
        background: #E7F1F2 !important;
        color: #021A23 !important;
    }
    
    /* Labels de los inputs - CLAROS para que se vean */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: #E7F1F2 !important;
        font-weight: 500 !important;
    }
    
    /* SOLO el valor del input oscuro, NO el label */
    .stNumberInput input {
        color: #021A23 !important;
    }
    
    /* Asegurar que TODOS los labels sean visibles */
    label {
        color: #E7F1F2 !important;
    }
    
    
    /* Selectbox dropdown y flechas */
    .stSelectbox > div > div > div {
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #021A23 !important;
    }
    
    /* Flecha del selectbox */
    .stSelectbox svg {
        color: #021A23 !important;
        fill: #021A23 !important;
    }
    
    /* Botones +- del number input */
    .stNumberInput button {
        color: #021A23 !important;
        background: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
    }
    
    .stNumberInput button:hover {
        background: #7B9E7E !important;
        color: #021A23 !important;
    }
    
    /* Progress bar personalizada con paleta Felmel */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #7B9E7E, #E7F1F2);
        border-radius: 8px;
        height: 12px;
    }
    
    .stProgress > div > div {
        background: #021A23;
        border-radius: 8px;
        border: 1px solid #7B9E7E;
    }
    
    /* Contenedor de progreso con paleta Felmel */
    .progress-container {
        background: #E7F1F2;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #7B9E7E;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 16px rgba(2, 26, 35, 0.3);
    }
    
    /* Estilo para imágenes clickeables */
    .stImage {
        cursor: pointer;
        border-radius: 5px;
        border: 1px solid #7B9E7E;
        transition: all 0.3s ease;
        background: #E7F1F2;
        padding: 2px;
        overflow: hidden;
    }
    
    .stImage:hover {
        border-color: #7B9E7E;
        box-shadow: 0 2px 8px rgba(123, 158, 126, 0.3);
        transform: scale(1.05);
    }
    
    /* Estilos para logo */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-sidebar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(123, 158, 126, 0.3);
    }
    
    .logo-header {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(123, 158, 126, 0.3);
        margin: 0 auto 1rem;
    }
    
    /* Ocultar botones de imagen que contienen solo espacio */
    .stButton > button[title="Clic para ampliar imagen"] {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        font-size: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        width: 0 !important;
        min-width: 0 !important;
        opacity: 0 !important;
        position: absolute !important;
        z-index: -1 !important;
    }
    
    .stButton > button[title="Clic para ampliar imagen"]:hover {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        opacity: 0 !important;
    }
    
    /* Botón de colapsar/expandir sidebar - más específico */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button,
    [data-testid="collapsedControl"] > button {
        background-color: #021A23 !important;
        color: #E7F1F2 !important;
        border: 1px solid #7B9E7E !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        transition: all 0.3s ease !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    [data-testid="collapsedControl"]:hover,
    [data-testid="collapsedControl"] button:hover,
    [data-testid="collapsedControl"] > button:hover {
        background-color: #7B9E7E !important;
        color: #021A23 !important;
        border-color: #E7F1F2 !important;
        transform: translateX(2px) !important;
    }
    
    /* Arreglar cursor invisible en campos de búsqueda */
    .stTextInput input {
        caret-color: #021A23 !important;
        cursor: text !important;
    }
    
    .stTextInput input:focus {
        caret-color: #021A23 !important;
        cursor: text !important;
    }
</style>
""", unsafe_allow_html=True)

# Estado de la sesión
if 'products_loaded' not in st.session_state:
    st.session_state.products_loaded = False
if 'df_orocolombia' not in st.session_state:
    st.session_state.df_orocolombia = pd.DataFrame()
if 'df_grupofelmel' not in st.session_state:
    st.session_state.df_grupofelmel = pd.DataFrame()
if 'df_new_products' not in st.session_state:
    st.session_state.df_new_products = pd.DataFrame()

# Estado para selecciones
if 'selected_new_products' not in st.session_state:
    st.session_state.selected_new_products = set()
if 'selected_all_products' not in st.session_state:
    st.session_state.selected_all_products = set()

def show_header():
    """Mostrar header principal con logo"""
    # Obtener logo procesado
    logo_base64 = get_logo_base64(logo_path)
    
    if logo_base64:
        st.markdown(f"""
        <div class="main-header">
            <div class="logo-header">
                <img src="{logo_base64}" width="80" height="80" alt="Felmel Logo">
            </div>
            <h1>Felmel Kardex</h1>
            <p>Grupo Felmel - Gestión de Inventario y Detección de Productos Nuevos</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Felmel Kardex</h1>
            <p>Grupo Felmel - Gestión de Inventario y Detección de Productos Nuevos</p>
        </div>
        """, unsafe_allow_html=True)

def show_image_modal(image_url, product_name):
    """Mostrar imagen en modal grande"""
    with st.expander(f"🖼️ {product_name}", expanded=True):
        try:
            st.image(image_url, caption=product_name, use_container_width=True)
            st.markdown(f"**URL de la imagen:** {image_url}")
        except Exception as e:
            st.error(f"❌ Error al cargar la imagen: {str(e)}")
            st.markdown(f"**URL:** {image_url}")

def show_dashboard_stats():
    """Mostrar estadísticas generales del dashboard"""
    if not st.session_state.products_loaded:
        st.info("⚠️ Carga primero los productos para ver estadísticas")
        return
    
    st.subheader("📊 Estadísticas del Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏪 OroColmbia")
        if not st.session_state.df_orocolombia.empty:
            df_oro = st.session_state.df_orocolombia
            
            # Productos con precio
            products_with_price = df_oro[df_oro['price'] > 0]
            
            st.metric("Total productos", len(df_oro))
            st.metric("Con precio válido", len(products_with_price))
            st.metric("Con imágenes", len(df_oro[df_oro['image_url'].notna() & (df_oro['image_url'] != '')]))
            
            if len(products_with_price) > 0:
                st.metric("Precio promedio", f"${products_with_price['price'].mean():,.0f}")
                st.metric("Valor total inventario", f"${products_with_price['price'].sum():,.0f}")
    
    with col2:
        st.markdown("### 🆕 Productos Nuevos")
        if not st.session_state.df_new_products.empty:
            df_new = st.session_state.df_new_products
            
            st.metric("Productos nuevos detectados", len(df_new))
            st.metric("Stock total disponible", f"{df_new['stock'].sum():,}")
            st.metric("Con imágenes", len(df_new[df_new['image_url'].notna() & (df_new['image_url'] != '')]))
            
            if len(df_new) > 0:
                st.metric("Valor total nuevos", f"${df_new['price'].sum():,.0f}")
                st.metric("Precio promedio nuevos", f"${df_new['price'].mean():,.0f}")
        else:
            st.info("🎉 No hay productos nuevos detectados")

def show_metrics():
    """Mostrar métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Productos nuevos va primero
        new_products_count = len(st.session_state.df_new_products) if not st.session_state.df_new_products.empty else 0
        st.metric(
            "🆕 Productos Nuevos",
            new_products_count
        )
    
    with col2:
        st.metric(
            "🏪 Productos OroColmbia",
            len(st.session_state.df_orocolombia) if not st.session_state.df_orocolombia.empty else 0
        )
    
    with col3:
        st.metric(
            "🏬 Productos GrupoFelmel",
            len(st.session_state.df_grupofelmel) if not st.session_state.df_grupofelmel.empty else 0
        )
    
    with col4:
        stock_value = 0
        if not st.session_state.df_new_products.empty:
            stock_value = st.session_state.df_new_products['stock'].sum()
        st.metric(
            "📦 Stock Disponible",
            f"{stock_value:,}"
        )

@st.cache_data(ttl=1800)  # Cache por 30 minutos
def fetch_products_cached():
    """Función cacheada para obtener productos"""
    product_manager = ProductManager()
    df_orocolombia, df_grupofelmel = product_manager.fetch_all_products()
    df_new_products = product_manager.find_new_products(df_orocolombia, df_grupofelmel)
    return df_orocolombia, df_grupofelmel, df_new_products

def load_products():
    """Cargar productos de ambas APIs con barra de progreso simplificada"""
    try:
        # Crear barra de progreso elegante
        progress_container = st.container()
        with progress_container:
            st.markdown("### 🚀 Cargando Productos")
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        def update_progress(percentage):
            """Actualizar progreso con porcentaje"""
            progress_bar.progress(percentage / 100)
            status_text.markdown(f"**Running... {percentage:.0f}%**")
        
        # Progreso inicial
        update_progress(5)
        time.sleep(0.1)
        
        # Intentar cargar desde cache primero
        try:
            # Cargar directamente sin mostrar el nombre de la función
            product_manager = ProductManager()
            df_orocolombia, df_grupofelmel = product_manager.fetch_all_products()
            df_new_products = product_manager.find_new_products(df_orocolombia, df_grupofelmel)
            
            # Simular progreso suave desde cache
            for i in range(10, 100, 3):
                update_progress(i)
                time.sleep(0.08)
            
        except Exception:
            # Si falla el cache, cargar desde APIs
            product_manager = ProductManager()
            
            # Progreso para OroColmbia
            update_progress(20)
            time.sleep(0.2)
            
            # Obtener productos
            df_orocolombia, df_grupofelmel = product_manager.fetch_all_products()
            
            # Progreso para GrupoFelmel
            update_progress(60)
            time.sleep(0.2)
            
            # Progreso para detección de productos nuevos
            update_progress(80)
            time.sleep(0.1)
            
            df_new_products = product_manager.find_new_products(df_orocolombia, df_grupofelmel)
        
        # Progreso final
        for i in range(90, 101, 2):
            update_progress(i)
            time.sleep(0.05)
        
        # Guardar en session state
        st.session_state.df_orocolombia = df_orocolombia
        st.session_state.df_grupofelmel = df_grupofelmel
        st.session_state.df_new_products = df_new_products
        st.session_state.products_loaded = True
        
        time.sleep(0.3)
        
        # Mostrar mensaje de éxito elegante
        st.markdown(f"""
        <div class="success-message">
            <strong>🎉 Consulta completada exitosamente</strong><br>
            🏪 <strong>OroColmbia:</strong> {len(df_orocolombia):,} productos<br>
            🏬 <strong>GrupoFelmel:</strong> {len(df_grupofelmel):,} productos<br>
            🆕 <strong>Productos nuevos:</strong> {len(df_new_products):,} productos
        </div>
        """, unsafe_allow_html=True)
        
        # Limpiar progreso después de 2 segundos
        time.sleep(2)
        progress_container.empty()
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            <strong>❌ Error al cargar productos</strong><br>
            {str(e)}
        </div>
        """, unsafe_allow_html=True)

@st.fragment
def show_new_products():
    """Mostrar tabla de productos nuevos optimizada"""
    if st.session_state.df_new_products.empty:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #1e2329; border-radius: 15px; border: 1px solid #30363d;">
            <h3 style="color: #00d4aa;">🎉 ¡No hay productos nuevos!</h3>
            <p style="color: #c9d1d9;">Tu inventario está actualizado</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### 🆕 Productos Nuevos Detectados")
    
    # Filtros en una sola fila para mejor UX
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            categories = ['Todas'] + sorted(st.session_state.df_new_products['categories'].unique().tolist())
            selected_category = st.selectbox("📂 Categoría", categories)
        
        with col2:
            # Obtener precio máximo real de los productos
            max_price_default = st.session_state.df_new_products['price'].max() if not st.session_state.df_new_products.empty else 1000000.0
            max_price = st.number_input("💰 Precio máximo", min_value=0.0, value=float(max_price_default), step=100.0)
        
        with col3:
            min_stock = st.number_input("📦 Stock mínimo", min_value=0, value=0, step=1)
        
        with col4:
            search_term = st.text_input("🔍 Buscar", placeholder="SKU o nombre...")
        
        with col5:
            # Paginación
            page_size_new = st.selectbox("📄 Mostrar", [50, 100, 200, 500, 1000, 2000], index=1, key="page_size_new")
    
    # Aplicar filtros optimizados
    df_filtered = st.session_state.df_new_products.copy()
    
    # Filtros de rendimiento
    if selected_category != 'Todas':
        df_filtered = df_filtered[df_filtered['categories'].str.contains(selected_category, na=False)]
    
    if search_term:
        df_filtered = df_filtered[
            df_filtered['name'].str.contains(search_term, case=False, na=False) |
            df_filtered['sku'].str.contains(search_term, case=False, na=False)
        ]
    
    # Aplicar filtros de precio y stock
    if max_price < max_price_default:  # Solo filtrar si el usuario cambió el precio
        df_filtered = df_filtered[df_filtered['price'] <= max_price]
    
    df_filtered = df_filtered[df_filtered['stock'] >= min_stock]
    
    # Paginación para rendimiento
    total_results_new = len(df_filtered)
    df_filtered = df_filtered.head(page_size_new)
    
    # Controles de selección
    if not df_filtered.empty:
        # Calcular productos seleccionados total
        total_selected = len(st.session_state.selected_new_products)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Seleccionar Todos", key="select_all_new"):
                st.session_state.selected_new_products.update(df_filtered['sku'].tolist())
                st.rerun()
        
        with col2:
            if st.button("❌ Deseleccionar Todos", key="deselect_all_new"):
                # Deseleccionar todos los productos de la vista actual
                for sku in df_filtered['sku'].tolist():
                    st.session_state.selected_new_products.discard(sku)
                st.rerun()
        
        with col3:
            if total_selected > 0:
                # Expandir opciones de exportación
                with st.expander("📥 Opciones de Exportación", expanded=False):
                    st.markdown("**Exportar productos seleccionados:**")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        create_download_button(
                            st.session_state.df_new_products,
                            list(st.session_state.selected_new_products),
                            "productos",
                            f"📋 Productos ({total_selected})",
                            "export_products_new"
                        )
                    
                    with col_b:
                        create_download_button(
                            st.session_state.df_new_products,
                            list(st.session_state.selected_new_products),
                            "urls",
                            f"🖼️ URLs Imágenes",
                            "export_urls_new"
                        )
                    
                    show_export_summary(df_filtered, list(st.session_state.selected_new_products))
            else:
                # Botón para exportar todos los productos nuevos
                with st.expander("📥 Exportar Todos los Productos Nuevos", expanded=False):
                    st.markdown("**Exportar todos los productos mostrados:**")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        create_download_button(
                            df_filtered,
                            None,  # Todos los productos
                            "productos",
                            f"📋 Todos los Productos ({len(df_filtered)})",
                            "export_all_products_new"
                        )
                    
                    with col_b:
                        create_download_button(
                            df_filtered,
                            None,
                            "urls",
                            f"🖼️ Todas las URLs",
                            "export_all_urls_new"
                        )
                    
                    show_export_summary(df_filtered, None)

    # Mostrar tabla con checkboxes
    if not df_filtered.empty:
        # Crear tabla personalizada con checkboxes
        st.markdown("### 📋 Selecciona los productos a exportar:")
        
        # Headers de la tabla
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.5, 0.8, 1, 2, 1.2, 1, 1, 0.8, 0.8])
        
        with col1:
            st.markdown("**☑️**")
        with col2:
            st.markdown("**🖼️ Imagen**")
        with col3:
            st.markdown("**SKU**")
        with col4:
            st.markdown("**Nombre**")
        with col5:
            st.markdown("**Categoría**")
        with col6:
            st.markdown("**Material**")
        with col7:
            st.markdown("**Precio**")
        with col8:
            st.markdown("**35% Desc.**")
        with col9:
            st.markdown("**Stock**")
        
        st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid #30363d;'>", unsafe_allow_html=True)
        
        # Contenedor para la tabla con scroll
        with st.container():
            for idx, row in df_filtered.iterrows():
                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.5, 0.8, 1, 2, 1.2, 1, 1, 0.8, 0.8])
                
                with col1:
                    # Checkbox para selección
                    def toggle_selection(sku):
                        if sku in st.session_state.selected_new_products:
                            st.session_state.selected_new_products.discard(sku)
                        else:
                            st.session_state.selected_new_products.add(sku)
                    
                    is_selected = row['sku'] in st.session_state.selected_new_products
                    checkbox_value = st.checkbox("Seleccionar", value=is_selected, key=f"new_{row['sku']}_{idx}", label_visibility="collapsed", on_change=toggle_selection, args=(row['sku'],))
                
                with col2:
                    # Mostrar imagen del producto clickeable
                    if row['image_url'] and row['image_url'] != '':
                        try:
                            # Mostrar imagen
                            st.image(
                                row['image_url'], 
                                width=50,
                                caption=None,
                                use_container_width=False
                            )
                        except:
                            st.text("❌")
                    else:
                        st.text("📷❌")
                
                with col3:
                    st.text(row['sku'])
                
                with col4:
                    # Truncar nombre
                    name = row['name'][:40] + '...' if len(row['name']) > 40 else row['name']
                    st.text(name)
                
                with col5:
                    category = row['categories'][:20] + '...' if len(row['categories']) > 20 else row['categories']
                    st.text(category)
                
                with col6:
                    material = row['material'][:15] + '...' if len(row['material']) > 15 else row['material']
                    st.text(material)
                
                with col7:
                    st.text(f"${row['price']:,.0f}")
                
                with col8:
                    st.text(f"${row['discount_price']:,.0f}")
                
                with col9:
                    st.text(str(row['stock']))
                
                # Separador sutil
                if idx < len(df_filtered) - 1:
                    st.markdown("<hr style='margin: 0.5rem 0; border: 0.5px solid #30363d;'>", unsafe_allow_html=True)
        
        # RECALCULAR después de los checkboxes
        total_selected = len(st.session_state.selected_new_products)
        
        # Mostrar controles de exportación
        st.markdown("---")
        st.markdown("### 📥 Opciones de Exportación")
        
        if total_selected > 0:
            st.markdown(f"**Exportar {total_selected} productos seleccionados:**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                create_download_button(
                    st.session_state.df_new_products,
                    list(st.session_state.selected_new_products),
                    "productos",
                    f"📋 Productos ({total_selected})",
                    "export_products_new_updated"
                )
            
            with col_b:
                create_download_button(
                    st.session_state.df_new_products,
                    list(st.session_state.selected_new_products),
                    "urls",
                    f"🖼️ URLs Imágenes ({total_selected})",
                    "export_urls_new_updated"
                )
            
            show_export_summary(st.session_state.df_new_products, list(st.session_state.selected_new_products))
        else:
            st.markdown("**Exportar todos los productos mostrados:**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                create_download_button(
                    df_filtered,
                    None,
                    "productos",
                    f"📋 Todos los Productos ({len(df_filtered)})",
                    "export_all_products_new"
                )
            
            with col_b:
                create_download_button(
                    df_filtered,
                    None,
                    "urls",
                    f"🖼️ Todas las URLs ({len(df_filtered)})",
                    "export_all_urls_new"
                )
            
            show_export_summary(df_filtered, None)
        
        # Estadísticas mejoradas
        total_value = df_filtered['price'].sum()
        avg_price = df_filtered['price'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Mostrando", f"{len(df_filtered):,}")
        with col2:
            st.metric("📈 Total disponible", f"{total_results_new:,}")
        with col3:
            if total_results_new > page_size_new:
                st.markdown(f"""
                <div style="background: #E7F1F2; padding: 1rem; border-radius: 8px; border: 1px solid #7B9E7E; margin: 0.5rem 0; color: #021A23;">
                    <strong>⚠️ Solo mostrando primeros {page_size_new} resultados</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #E7F1F2; padding: 1rem; border-radius: 8px; border: 1px solid #7B9E7E; margin: 0.5rem 0; color: #021A23;">
                    <strong>✅ Todos los resultados mostrados</strong>
                </div>
                """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ No hay productos que coincidan con los filtros seleccionados.")

@st.fragment
def show_all_products():
    """Mostrar todos los productos de OroColmbia optimizada"""
    if st.session_state.df_orocolombia.empty:
        st.info("📦 No hay productos cargados.")
        return
    
    st.markdown("### 📋 Catálogo Completo - OroColmbia")
    
    # Filtros optimizados en una fila
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            categories = ['Todas'] + sorted(st.session_state.df_orocolombia['categories'].unique().tolist())
            selected_category = st.selectbox("📂 Categoría", categories, key="all_products_category")
        
        with col2:
            # Obtener precio máximo real de todos los productos
            max_price_default_all = st.session_state.df_orocolombia['price'].max() if not st.session_state.df_orocolombia.empty else 1000000.0
            max_price = st.number_input("💰 Precio máximo", min_value=0.0, value=float(max_price_default_all), step=100.0, key="all_products_price")
        
        with col3:
            min_stock = st.number_input("📦 Stock mínimo", min_value=0, value=0, step=1, key="all_products_stock")
        
        with col4:
            search_term = st.text_input("🔍 Buscar", placeholder="SKU o nombre...", key="all_search")
        
        with col5:
            # Paginación
            page_size = st.selectbox("📄 Mostrar", [50, 100, 200, 500, 1000, 2000], index=1, key="page_size")
    
    # Aplicar filtros con mejor rendimiento
    df_filtered = st.session_state.df_orocolombia.copy()
    
    if search_term:
        df_filtered = df_filtered[
            df_filtered['name'].str.contains(search_term, case=False, na=False) |
            df_filtered['sku'].str.contains(search_term, case=False, na=False)
        ]
    
    if selected_category != 'Todas':
        df_filtered = df_filtered[df_filtered['categories'].str.contains(selected_category, na=False)]
    
    if max_price < max_price_default_all:  # Solo filtrar si el usuario cambió el precio
        df_filtered = df_filtered[df_filtered['price'] <= max_price]
    
    df_filtered = df_filtered[df_filtered['stock'] >= min_stock]
    
    # Paginación para rendimiento
    total_results = len(df_filtered)
    df_filtered = df_filtered.head(page_size)
    
    # Controles de selección para todos los productos
    if not df_filtered.empty:
        # Calcular productos seleccionados que están en la vista actual
        selected_in_view_all = [sku for sku in st.session_state.selected_all_products if sku in df_filtered['sku'].tolist()]
        selected_count_all = len(selected_in_view_all)
        total_selected_all = len(st.session_state.selected_all_products)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Seleccionar Todos", key="select_all_products"):
                st.session_state.selected_all_products.update(df_filtered['sku'].tolist())
                st.rerun()
        
        with col2:
            if st.button("❌ Deseleccionar Todos", key="deselect_all_products"):
                # Deseleccionar todos los productos de la vista actual
                for sku in df_filtered['sku'].tolist():
                    st.session_state.selected_all_products.discard(sku)
                st.rerun()
        
        with col3:
            if total_selected_all > 0:
                # Expandir opciones de exportación
                with st.expander("📥 Opciones de Exportación", expanded=False):
                    st.markdown("**Exportar productos seleccionados:**")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        create_download_button(
                            st.session_state.df_orocolombia,  # Todos los productos, no solo la vista
                            list(st.session_state.selected_all_products),
                            "productos",
                            f"📋 Productos ({total_selected_all})",
                            "export_products_all"
                        )
                    
                    with col_b:
                        create_download_button(
                            st.session_state.df_orocolombia,  # Todos los productos, no solo la vista
                            list(st.session_state.selected_all_products),
                            "urls",
                            f"🖼️ URLs Imágenes",
                            "export_urls_all"
                        )
                    
                    show_export_summary(df_filtered, list(st.session_state.selected_all_products))
            else:
                # Botón para exportar todos los productos
                with st.expander("📥 Exportar Todos los Productos", expanded=False):
                    st.markdown("**Exportar todos los productos mostrados:**")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        create_download_button(
                            df_filtered,
                            None,
                            "productos",
                            f"📋 Todos los Productos ({len(df_filtered)})",
                            "export_all_products_catalog"
                        )
                    
                    with col_b:
                        create_download_button(
                            df_filtered,
                            None,
                            "urls",
                            f"🖼️ Todas las URLs",
                            "export_all_urls_catalog"
                        )
                    
                    show_export_summary(df_filtered, None)

    # Mostrar tabla con checkboxes para todos los productos
    if not df_filtered.empty:
        st.markdown("### 📋 Selecciona los productos del catálogo:")
        
        # Headers de la tabla
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([0.5, 0.8, 1, 2, 1.2, 1, 1, 0.8])
        
        with col1:
            st.markdown("**☑️**")
        with col2:
            st.markdown("**🖼️ Imagen**")
        with col3:
            st.markdown("**SKU**")
        with col4:
            st.markdown("**Nombre**")
        with col5:
            st.markdown("**Categoría**")
        with col6:
            st.markdown("**Material**")
        with col7:
            st.markdown("**Precio**")
        with col8:
            st.markdown("**35% Desc.**")
        
        st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid #30363d;'>", unsafe_allow_html=True)
        
        # Contenedor para la tabla con scroll
        with st.container():
            for idx, row in df_filtered.iterrows():
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([0.5, 0.8, 1, 2, 1.2, 1, 1, 0.8])
                
                with col1:
                    # Checkbox para selección
                    def toggle_selection_all(sku):
                        if sku in st.session_state.selected_all_products:
                            st.session_state.selected_all_products.discard(sku)
                        else:
                            st.session_state.selected_all_products.add(sku)
                    
                    is_selected = row['sku'] in st.session_state.selected_all_products
                    checkbox_value = st.checkbox("Seleccionar", value=is_selected, key=f"all_{row['sku']}_{idx}", label_visibility="collapsed", on_change=toggle_selection_all, args=(row['sku'],))
                
                with col2:
                    # Mostrar imagen del producto clickeable
                    if row['image_url'] and row['image_url'] != '':
                        try:
                            # Mostrar imagen
                            st.image(
                                row['image_url'], 
                                width=50,
                                caption=None,
                                use_container_width=False
                            )
                        except:
                            st.text("❌")
                    else:
                        st.text("📷❌")
                
                with col3:
                    st.text(row['sku'])
                
                with col4:
                    name = row['name'][:40] + '...' if len(row['name']) > 40 else row['name']
                    st.text(name)
                
                with col5:
                    category = row['categories'][:20] + '...' if len(row['categories']) > 20 else row['categories']
                    st.text(category)
                
                with col6:
                    material = row['material'][:15] + '...' if len(row['material']) > 15 else row['material']
                    st.text(material)
                
                with col7:
                    st.text(f"${row['price']:,.0f}")
                
                with col8:
                    st.text(f"${row['discount_price']:,.0f}")
                
                # Separador sutil
                if idx < len(df_filtered) - 1:
                    st.markdown("<hr style='margin: 0.5rem 0; border: 0.5px solid #30363d;'>", unsafe_allow_html=True)
        
        # Estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Mostrando", f"{len(df_filtered):,}")
        with col2:
            st.metric("📈 Total disponible", f"{total_results:,}")
        with col3:
            if total_results > page_size:
                st.markdown(f"""
                <div style="background: #E7F1F2; padding: 1rem; border-radius: 8px; border: 1px solid #7B9E7E; margin: 0.5rem 0; color: #021A23;">
                    <strong>⚠️ Solo mostrando primeros {page_size} resultados</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #E7F1F2; padding: 1rem; border-radius: 8px; border: 1px solid #7B9E7E; margin: 0.5rem 0; color: #021A23;">
                    <strong>✅ Todos los resultados mostrados</strong>
                </div>
                """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ No hay productos que coincidan con los filtros seleccionados.")

def main():
    """Función principal"""
    show_header()
    
    # Sidebar con logo
    logo_base64_sidebar = get_logo_base64(logo_path)
    
    if logo_base64_sidebar:
        st.sidebar.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="margin-bottom: 0.5rem;">
                <img src="{logo_base64_sidebar}" width="80" height="80" alt="Felmel Logo">
            </div>
            <div style="color: #021a23; font-size: 1.4rem; font-weight: 600;">
                Felmel Kardex
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.title("🚀 Felmel Kardex")
    
    st.sidebar.markdown("---")
    
    # Botones de acción principales
    if not st.session_state.products_loaded:
        if st.sidebar.button("Cargar Productos", use_container_width=True, type="primary"):
            load_products()
    else:
        if st.sidebar.button("🔄 Actualizar", use_container_width=True, type="primary"):
            with st.spinner("Limpiando cache..."):
                st.session_state.products_loaded = False
                st.session_state.df_orocolombia = pd.DataFrame()
                st.session_state.df_grupofelmel = pd.DataFrame()
                st.session_state.df_new_products = pd.DataFrame()
                # Limpiar selecciones
                st.session_state.selected_new_products = set()
                st.session_state.selected_all_products = set()
                st.rerun()
    
    # Navegación
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navegación")
    
    # Pestañas profesionales como botones
    st.markdown("""
    <style>
    .tab-button {
        background: #1e2329;
        color: #c9d1d9;
        border: 1px solid #30363d;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.2rem 0;
        width: 100%;
        text-align: left;
    }
    .tab-button:hover {
        background: #262d34;
        border-color: #00d4aa;
    }
    .tab-button.active {
        background: linear-gradient(45deg, #00d4aa, #00f5cc);
        color: #0e1117;
        border-color: #00d4aa;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    pages = ["🏠 Inicio", "🆕 Productos Nuevos", "📦 Todos los Productos", "📊 Estadísticas", "📋 Historial", "⚙️ Configuración"]
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Inicio"
    
    for page_name in pages:
        if st.sidebar.button(page_name, key=f"tab_{page_name}", use_container_width=True):
            st.session_state.current_page = page_name
            st.rerun()
    
    page = st.session_state.current_page
    
    # Mostrar métricas si hay datos
    if st.session_state.products_loaded:
        show_metrics()
        st.markdown("---")
    
    # Mostrar página seleccionada
    if page == "🏠 Inicio":
        if st.session_state.products_loaded:
            st.markdown("""
            <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
                <strong>✅ Datos cargados correctamente</strong><br>
                Utiliza el menú lateral para navegar.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
                <strong>👋 Bienvenido al Felmel Kardex</strong><br>
                Haz clic en 'Cargar Productos' para empezar.
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "🆕 Productos Nuevos":
        if st.session_state.products_loaded:
            show_new_products()
        else:
            st.markdown("""
            <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
                <strong>⚠️ Primero debes cargar los productos</strong><br>
                Usa el botón 'Cargar Productos' en la barra lateral.
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📦 Todos los Productos":
        if st.session_state.products_loaded:
            show_all_products()
        else:
            st.markdown("""
            <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
                <strong>⚠️ Primero debes cargar los productos</strong><br>
                Usa el botón 'Cargar Productos' en la barra lateral.
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📊 Estadísticas":
        if st.session_state.products_loaded:
            show_dashboard_stats()
        else:
            st.markdown("""
            <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
                <strong>⚠️ Primero debes cargar los productos</strong><br>
                Usa el botón 'Cargar Productos' en la barra lateral.
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📋 Historial":
        st.subheader("📋 Historial de Exportaciones")
        st.markdown("""
        <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
            <strong>🚧 Próximamente</strong><br>
            Historial de exportaciones con calendario.
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "⚙️ Configuración":
        st.subheader("⚙️ Configuración")
        st.markdown("""
        <div style="background: #E7F1F2; padding: 1.5rem; border-radius: 10px; border: 1px solid #7B9E7E; margin: 1rem 0; color: #021A23;">
            <strong>🚧 Próximamente</strong><br>
            Configuración de APIs y parámetros.
        </div>
        """, unsafe_allow_html=True)
    
    # Footer elegante
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: #1e2329; border-radius: 10px; border: 1px solid #30363d;">
        <h4 style="color: #00d4aa; margin: 0;">Kardex</h4>
        <p style="color: #c9d1d9; margin: 0.5rem 0; font-size: 0.9rem;">Grupo Felmel</p>
        <p style="color: #8b949e; margin: 0; font-size: 0.8rem;">v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()