@echo off
REM Build and Run AI Product Advisor Docker Container
echo ================================
echo AI Product Advisor - Docker Setup
echo ================================
echo.

echo [1/3] Building Docker image...
docker-compose build

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting containers...
docker-compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start containers!
    pause
    exit /b 1
)

echo.
echo [3/3] Waiting for services to initialize...
timeout /t 10 /nobreak > nul

echo.
echo ================================
echo ✅ SUCCESS!
echo ================================
echo.
echo 📓 Jupyter Notebook: http://localhost:8888
echo 🤖 Ollama API: http://localhost:11434
echo.
echo Note: First startup will download ~13GB model (gpt-oss:20b)
echo This may take 10-30 minutes depending on your internet speed.
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo.
pause

