# 🚀 Guía de Despliegue en Streamlit Cloud

## Paso a Paso para Configurar tu Dashboard Kardex

### 1. 📋 Verificar que el código esté en GitHub
✅ **Ya está hecho** - Tu repositorio está en: `https://github.com/Programmerdj20/dashboard-kardex-felmel`

### 2. 🔗 Conectar con Streamlit Cloud

1. **Ve a:** https://share.streamlit.io
2. **Inicia sesión** con tu cuenta de GitHub
3. **Haz clic en "New app"**
4. **Selecciona tu repositorio:** `Programmerdj20/dashboard-kardex-felmel`
5. **Configuración:**
   - **Branch:** `main`
   - **Main file path:** `main.py`
   - **App URL:** (puedes personalizar o dejar el por defecto)

### 3. 🔐 Configurar Secrets (MUY IMPORTANTE)

1. **Antes de hacer deploy**, haz clic en **"Advanced settings"**
2. **Secrets:** Copia y pega EXACTAMENTE esto:

```toml
OROCOLOMBIA_URL = "https://orocolombia.co/wp-json/wc/v3/products"
OROCOLOMBIA_CONSUMER_KEY = "ck_865f2431376662f2bff8e2fdca6a933869805784"
OROCOLOMBIA_CONSUMER_SECRET = "cs_b4d4ae6ce65cfa4300464afa935cc708398b90b4"
GRUPOFELMEL_URL = "https://app.grupofelmel.com/wp-json/wc/v3/products"
GRUPOFELMEL_CONSUMER_KEY = "ck_ea825feef0c11159e9c95c4e410a76f800f4c38f"
GRUPOFELMEL_CONSUMER_SECRET = "cs_693ed6a9afb56a24d1c55fcbeb39f3bd2423818d"
PRODUCTS_PER_PAGE = 100
CACHE_DURATION_MINUTES = 30
DISCOUNT_PERCENTAGE = 35
```

3. **Haz clic en "Save"**
4. **Haz clic en "Deploy!"**

### 4. 🎯 Si ya tienes la app desplegada pero sin secrets:

1. **Ve a tu app en Streamlit Cloud**
2. **Haz clic en "Settings" (⚙️)**
3. **Selecciona "Secrets"**
4. **Pega el contenido de arriba**
5. **Haz clic en "Save"**
6. **Reinicia tu app:** Settings → "Reboot app"

### 5. ✅ Verificar que funcione

Una vez configurado, tu app debería:
- ✅ Cargar sin errores de variables de entorno
- ✅ Mostrar el botón "Cargar Productos"
- ✅ Conectar con las APIs exitosamente

### 6. 🐛 Solución de problemas

**Si sigues viendo errores:**

1. **Verifica que los secrets estén exactamente como se muestra arriba**
2. **Asegúrate de que no haya espacios extra**
3. **Verifica que las credenciales de API sean correctas**
4. **Reinicia la app después de cambiar secrets**

**Para verificar secrets:**
- Ve a Settings → Secrets
- Deberías ver todas las variables listadas

### 7. 📱 URL de tu app

Una vez desplegada, tu app estará disponible en:
`https://dashboard-kardex-felmel.streamlit.app/` (o la URL que hayas personalizado)

---

## 💡 Notas importantes:

- **Los secrets NUNCA se suben a GitHub** (están en .gitignore)
- **Solo tú puedes ver los secrets** de tu app
- **Reinicia la app** después de cambiar secrets
- **El primer despliegue puede tardar 2-3 minutos**

## 🆘 ¿Necesitas ayuda?

Si tienes problemas:
1. Verifica que los secrets estén configurados correctamente
2. Reinicia la app
3. Revisa los logs en Streamlit Cloud para errores específicos