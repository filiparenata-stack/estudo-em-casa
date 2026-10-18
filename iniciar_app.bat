@echo off
chcp 65001 > nul
title Escola Virtual 7.º Ano - Assistente de Estudo e Quizzes
echo ===================================================================
echo       ESCOLA VIRTUAL 7.º ANO - ASSISTENTE DE ESTUDO E QUIZZES
echo ===================================================================
echo.
echo A iniciar servidor local...

set "ROOT_APP=%~dp0"
cd /d "%ROOT_APP%backend"

REM Abrir navegador automaticamente após 2 segundos
start "" cmd /c "timeout /t 2 /nobreak > nul && start http://127.0.0.1:8000"

echo.
echo ===================================================================
echo   APLICAÇÃO PRONTA! Abre o navegador em: http://127.0.0.1:8000
echo   Pressiona Ctrl+C nesta janela quando quiseres encerrar.
echo ===================================================================
echo.
"%ROOT_APP%.venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
