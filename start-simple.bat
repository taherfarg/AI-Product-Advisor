@echo off
echo ================================================
echo AI Product Advisor - Simple Web App
echo ================================================
echo.
echo This uses your EXISTING Ollama installation
echo No need to run Ollama in Docker!
echo.

echo [1/2] Building web app...
docker-compose -f docker-compose.simple.yml build

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Starting web app...
docker-compose -f docker-compose.simple.yml up -d

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start!
    pause
    exit /b 1
)

echo.
echo ================================================
echo ✅ SUCCESS!
echo ================================================
echo.
echo 🌐 Web App: http://localhost:8501
echo 🤖 Using Ollama from your system
echo.
echo Opening browser...
timeout /t 3 /nobreak > nul
start http://localhost:8501

echo.
echo To stop:
echo   docker-compose -f docker-compose.simple.yml down
echo.
pause

