@echo off
title LinkedIn Automation - Sistema de Publicación Automática
color 0A

echo =============================================
echo  LINKEDIN AUTOMATION - SISTEMA LOCAL
echo =============================================
echo.

echo Verificando instalación de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado.
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado

echo.
echo Instalando dependencias...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo [ADVERTENCIA] Algunas dependencias pueden no haberse instalado.
    echo La aplicación funcionará con funcionalidad limitada.
)

echo.
echo Creando directorios necesarios...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "assets" mkdir assets
if not exist "assets\images" mkdir assets\images

echo.
echo =============================================
echo  INICIANDO APLICACIÓN...
echo =============================================
echo.

python linkedin_automation.py

if errorlevel 1 (
    echo.
    echo [ERROR] La aplicación se cerró con errores.
    echo Revisa el archivo logs/app.log para más detalles.
    pause
)

echo.
echo Aplicación cerrada.
pause