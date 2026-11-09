@echo off
setlocal
cd /d "%~dp0"

echo ===================================================================
echo     ESCOLA VIRTUAL 8. ANO - EXTRATOR DE MANUAIS E TESTES
echo ===================================================================
echo.
echo 1. A verificar dependencias do Python (Playwright, Pillow, pypdf)...
echo.

set "PYTHON_EXE="

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=py"
    ) else (
        where python >nul 2>nul
        if not errorlevel 1 (
            set "PYTHON_EXE=python"
        ) else (
            for /f "delims=" %%I in ('where /r "%LOCALAPPDATA%\Programs\Python" python.exe 2^>nul') do (
                if not defined PYTHON_EXE set "PYTHON_EXE=%%I"
            )
        )
    )
)

if not defined PYTHON_EXE (
    echo [ERRO] O Python nao foi encontrado no teu computador!
    echo Por favor, instala o Python a partir de https://www.python.org/downloads/
    echo Certifica-te de marcar a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo Python detetado: %PYTHON_EXE%
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
