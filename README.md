# Dashboard Kardex - Grupo Felmel

Dashboard minimalista para comparación de productos entre OroColmbia (proveedor) y GrupoFelmel (tienda).

## Características

- 🆕 **Detección de productos nuevos** - Identifica productos con stock que no están en tu tienda
- 🖼️ **Visualización de imágenes** - Muestra imágenes de productos con zoom
- ✅ **Selección múltiple** - Selecciona productos específicos para exportar
- 📊 **Exportación inteligente** - Exporta productos o URLs de imágenes
- 📈 **Historial de exportaciones** - Rastrea exportaciones por fecha
- 🔍 **Filtros avanzados** - Filtra por categoría, precio, material, etc.
- 💰 **Cálculo de descuentos** - Calcula precios con 35% de descuento

## Instalación

1. **Crear entorno virtual:**
```bash
python -m venv venv
```

2. **Activar entorno virtual:**
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Uso

### Iniciar Dashboard
```bash
# Opción 1: Script automático (recomendado)
./start.sh

# Opción 2: Manual
source venv/bin/activate
streamlit run src/main.py
```

### Reiniciar Dashboard
```bash
./restart.sh
```

### Detener Dashboard
```bash
./stop.sh
```

### URLs de acceso
- **Local**: http://localhost:8501
- **Red local**: http://TU_IP:8501

## Estructura del proyecto

```
dashboard-felmel/
├── src/                 # Código fuente
├── pages/              # Páginas de Streamlit
├── exports/            # Archivos exportados
├── data/              # Cache y base de datos
├── tests/             # Pruebas
├── .env               # Variables de entorno
└── requirements.txt   # Dependencias
```

## 🚀 Despliegue en Streamlit Cloud

### Configuración rápida:

1. **Fork este repositorio en GitHub**
2. **Conecta con Streamlit Cloud**:
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona este repositorio
   - Archivo principal: `main.py`

3. **Configura las variables de entorno** en Streamlit Cloud:
   ```toml
   # En la sección "Secrets" de tu app
   OROCOLOMBIA_URL = "https://orocolombia.co/wp-json/wc/v3/products"
   OROCOLOMBIA_CONSUMER_KEY = "tu_consumer_key"
   OROCOLOMBIA_CONSUMER_SECRET = "tu_consumer_secret"
   GRUPOFELMEL_URL = "https://app.grupofelmel.com/wp-json/wc/v3/products"
   GRUPOFELMEL_CONSUMER_KEY = "tu_consumer_key"
   GRUPOFELMEL_CONSUMER_SECRET = "tu_consumer_secret"
   PRODUCTS_PER_PAGE = 100
   CACHE_DURATION_MINUTES = 30
   DISCOUNT_PERCENTAGE = 35
   ```

4. **¡Despliega!** - Tu app estará disponible en unos minutos

## Despliegue en Hostinger

El proyecto está optimizado para desplegarse en servidores Hostinger con soporte para Python.

## Tecnologías

- **Frontend**: Streamlit
- **Backend**: Python
- **Base de datos**: SQLite
- **APIs**: WooCommerce REST API
- **Exportación**: CSV/Excel