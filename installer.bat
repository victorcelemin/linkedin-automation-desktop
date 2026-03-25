@echo off
title LinkedIn Automation - Instalador
color 0B

echo =============================================
echo  INSTALADOR LINKEDIN AUTOMATION
echo  Sistema de Publicación Automática
echo =============================================
echo.

:: Check admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Permisos de administrador
) else (
    echo [INFO] Instalando para el usuario actual...
)

:: Create installation directory
set INSTALL_DIR=%LOCALAPPDATA%\LinkedInAutomation
echo.
echo Creando directorio de instalación...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy files
echo.
echo Copiando archivos...
xcopy /E /Y /Q "dist\*" "%INSTALL_DIR%\" >nul
xcopy /E /Y /Q "modules" "%INSTALL_DIR%\modules\" >nul
xcopy /E /Y /Q "assets" "%INSTALL_DIR%\assets\" >nul
xcopy /E /Y /Q "data" "%INSTALL_DIR%\data\" >nul

:: Create desktop shortcut
echo.
echo Creando acceso directo en el escritorio...
set SHORTCUT="%USERPROFILE%\Desktop\LinkedIn Automation.lnk"
echo Set WshShell = CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set Shortcut = WshShell.CreateShortcut(%SHORTCUT%) >> CreateShortcut.vbs
echo Shortcut.TargetPath = "%INSTALL_DIR%\LinkedIn_Automation.exe" >> CreateShortcut.vbs
echo Shortcut.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo Shortcut.Description = "LinkedIn Automation - Sistema de Publicación Automática" >> CreateShortcut.vbs
echo Shortcut.IconLocation = "%INSTALL_DIR%\assets\icon.ico,0" >> CreateShortcut.vbs
echo Shortcut.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

:: Create Start Menu shortcut
echo.
echo Creando acceso en menú inicio...
set STARTMENU="%APPDATA%\Microsoft\Windows\Start Menu\Programs\LinkedIn Automation"
if not exist %STARTMENU% mkdir %STARTMENU%
echo Set WshShell = CreateObject("WScript.Shell") > CreateShortcut2.vbs
echo Set Shortcut = WshShell.CreateShortcut("%STARTMENU%\LinkedIn Automation.lnk") >> CreateShortcut2.vbs
echo Shortcut.TargetPath = "%INSTALL_DIR%\LinkedIn_Automation.exe" >> CreateShortcut2.vbs
echo Shortcut.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut2.vbs
echo Shortcut.Description = "LinkedIn Automation" >> CreateShortcut2.vbs
echo Shortcut.IconLocation = "%INSTALL_DIR%\assets\icon.ico,0" >> CreateShortcut2.vbs
echo Shortcut.Save >> CreateShortcut2.vbs
cscript //nologo CreateShortcut2.vbs
del CreateShortcut2.vbs

:: Create uninstaller
echo.
echo Creando desinstalador...
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo echo Desinstalando LinkedIn Automation... >> "%INSTALL_DIR%\uninstall.bat"
echo echo. >> "%INSTALL_DIR%\uninstall.bat"
echo echo Eliminando archivos... >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /S /Q "%INSTALL_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo echo Eliminando accesos directos... >> "%INSTALL_DIR%\uninstall.bat"
echo del "%USERPROFILE%\Desktop\LinkedIn Automation.lnk" 2^>nul >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /S /Q "%STARTMENU%" 2^>nul >> "%INSTALL_DIR%\uninstall.bat"
echo echo. >> "%INSTALL_DIR%\uninstall.bat"
echo echo LinkedIn Automation ha sido desinstalado. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

echo.
echo =============================================
echo  INSTALACIÓN COMPLETADA
echo =============================================
echo.
echo LinkedIn Automation ha sido instalado en:
echo %INSTALL_DIR%
echo.
echo Accesos creados:
echo   - Escritorio
echo   - Menú Inicio
echo.
echo Para desinstalar, ejecuta uninstall.bat
echo en la carpeta de instalación.
echo.
echo ¿Deseas iniciar la aplicación ahora? (S/N)
set /p choice=
if /i "%choice%"=="S" (
    start "" "%INSTALL_DIR%\LinkedIn_Automation.exe"
)

echo.
echo ¡Gracias por instalar LinkedIn Automation!
pause