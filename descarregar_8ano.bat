@echo off
setlocal
cd /d "%~dp0"

echo ===================================================================
echo     ESCOLA VIRTUAL 8. ANO - EXTRATOR DE MANUAIS E TESTES
echo ===================================================================
echo.
echo 0. A atualizar codigo do GitHub (git pull origin main)...
where git >nul 2>nul
if not errorlevel 1 (
    git pull origin main
) else (
    echo [Aviso] git nao encontrado no PATH, a continuar com ficheiros locais...
)
echo.
echo 1. A verificar dependencias do Python (Pillow, pypdf)...
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
"%PYTHON_EXE%" -c "import PIL, pypdf" >nul 2>nul || "%PYTHON_EXE%" -m pip install --upgrade pillow pypdf

echo.
echo 2. A iniciar interface grafica do extrator Escola Virtual...
echo.

"%PYTHON_EXE%" "%~dp0scripts\gui_extrator_escola_virtual.py"

echo.
echo ===================================================================
echo Processo concluido! Prime qualquer tecla para sair.
echo ===================================================================
pause
