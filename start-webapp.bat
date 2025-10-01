@echo off
REM Start AI Product Advisor Web App with Ollama

echo ================================================
echo AI Product Advisor - Streamlit Web App
echo ================================================
echo.

echo [Step 1/4] Starting Ollama service...
docker-compose -f docker-compose.webapp.yml up -d ollama

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start Ollama!
    pause
    exit /b 1
)

echo Waiting for Ollama to initialize (30 seconds)...
timeout /t 30 /nobreak > nul

echo.
echo [Step 2/4] Pulling gpt-oss:20b model...
docker exec ollama-server ollama pull gpt-oss:20b

echo.
echo [Step 3/4] Building web app...
docker-compose -f docker-compose.webapp.yml build webapp

echo.
echo [Step 4/4] Starting web app...
docker-compose -f docker-compose.webapp.yml up -d webapp

echo.
echo ================================================
echo ✅ SUCCESS! Services are running
echo ================================================
echo.
echo 🌐 Web App: http://localhost:8501
echo 🤖 Ollama API: http://localhost:11434
echo.
echo To view logs:
echo   docker-compose -f docker-compose.webapp.yml logs -f
echo.
echo To stop:
echo   docker-compose -f docker-compose.webapp.yml down
echo.
echo Opening web browser...
timeout /t 3 /nobreak > nul
start http://localhost:8501

pause

