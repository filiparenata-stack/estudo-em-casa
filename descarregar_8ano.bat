@echo off
setlocal
cd /d "%~dp0"

echo ===================================================================
echo     ESCOLA VIRTUAL 8. ANO - EXTRATOR DE MANUAIS E TESTES
echo ===================================================================
echo.
echo 1. A verificar dependencias do Python (Playwright, Pillow, pypdf)...
echo.

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" -m pip install --upgrade playwright pillow pypdf
"%PYTHON_EXE%" -m playwright install chromium

echo.
echo 2. A iniciar extrator com navegador controlado...
echo.

"%PYTHON_EXE%" "%~dp0scripts\descarregar_escola_virtual_8ano.py"

echo.
echo ===================================================================
echo Processo concluido! Prime qualquer tecla para sair.
echo ===================================================================
pause
