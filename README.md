# LinkedIn Automation - Aplicación Local

Aplicación de escritorio para automatizar publicaciones en LinkedIn con comportamiento humano.

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Windows)
1. Doble clic en `start.bat`
2. Esperar a que se instalen las dependencias
3. La aplicación se abrirá automáticamente

### Opción 2: Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python linkedin_automation.py
```

## 📋 Requisitos

- Python 3.8 o superior
- Chrome Browser (para Selenium)
- Cuenta de LinkedIn

## 🎯 Características

### ✅ Dashboard
- Estadísticas en tiempo real
- Posts recientes
- Acciones rápidas

### ✅ Generador de Contenido
- 5 temas: Reflexión, Educación, Motivación, Técnico, Experiencia
- Variaciones únicas cada vez
- Vista previa con imagen
- Hashtags automáticos

### ✅ Gestión de Posts
- Lista completa de posts
- Filtrado por estado
- Acciones: Publicar, Programar, Editar, Eliminar

### ✅ Programación Inteligente
- Frecuencia: 3-5 posts por semana
- Horarios variables (mañana, tarde, noche)
- Evita fines de semana (80%)
- Horarios aleatorios (ej: 8:13, 12:47, 18:05)

### ✅ Conexión LinkedIn
- Login automático con Selenium
- Comportamiento humano (delays, scroll, typos raros)
- Publicación directa

### ✅ Base de Datos Local
- SQLite para almacenamiento local
- Sin dependencia de servicios externos
- Backup automático

## 📁 Estructura

```
linkedin-local-app/
├── linkedin_automation.py  # Aplicación principal
├── requirements.txt        # Dependencias
├── start.bat              # Script de inicio (Windows)
├── modules/
│   ├── database.py        # Base de datos SQLite
│   ├── content_generator.py  # Generación de contenido
│   ├── image_handler.py   # Manejo de imágenes
│   ├── scheduler.py       # Programación inteligente
│   └── linkedin_automation.py # Automatización LinkedIn
├── data/                  # Datos y configuración
├── logs/                  # Archivos de log
└── assets/               # Recursos
```

## 🔧 Configuración

1. **Credenciales LinkedIn**: Configurar en la pestaña Configuración
2. **Perfil**: Nombre, industria, temas principales
3. **Automatización**: Delay, nivel de comportamiento
4. **Programación**: Posts por semana, horarios preferidos

## ⚠️ Notas Importantes

- La aplicación usa Selenium con Chrome
- Los delays simulan comportamiento humano
- Los typos ocasionales son intencionales
- Los datos se guardan localmente en SQLite

## 🛡️ Seguridad

- Las credenciales se guardan localmente
- No se envían datos a servidores externos
- Solo se conecta a linkedin.com

## 📊 Estado

- ✅ Aplicación funcional
- ✅ Interfaz gráfica completa
- ✅ Base de datos SQLite
- ✅ Generación de contenido
- ✅ Conexión LinkedIn (requiere Chrome)
- ✅ Programación inteligente