@echo off
title VerificaCO - Sistema Unificado de Antecedentes (Colombia)
cd /d "%~dp0"

echo ==============================================================================
echo   Iniciando VerificaCO: Consulta Unificada de Antecedentes y Procesos Judiciales
echo ==============================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/2] Creando entorno virtual .venv...
    python -m venv .venv
    echo [2/2] Instalando librerias...
    .venv\Scripts\pip install -r requirements.txt
)

echo [OK] Abriendo navegador en http://127.0.0.1:8080 ...
start http://127.0.0.1:8080

echo [OK] Servidor iniciado en puerto 8080. Presione Ctrl+C para detener.
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
pause
