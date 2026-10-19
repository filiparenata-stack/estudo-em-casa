@echo off
setlocal
cd /d "%~dp0"

echo ===================================================================
echo       ESCOLA VIRTUAL 7. ANO - ASSISTENTE DE ESTUDO E QUIZZES
echo ===================================================================
echo.
echo A iniciar servidor local...
echo.

start "" cmd /c "timeout /t 2 /nobreak > nul && start http://127.0.0.1:8000"

echo ===================================================================
echo   APLICACAO PRONTA! O navegador vai abrir em: http://127.0.0.1:8000
echo   Pressiona Ctrl+C nesta janela quando quiseres encerrar.
echo ===================================================================
echo.

"%~dp0.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
