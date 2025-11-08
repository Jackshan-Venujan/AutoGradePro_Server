@echo off
REM AutoGradePro Performance Testing Setup and Runner
REM Windows PowerShell/CMD Script

echo ============================================================
echo AutoGradePro Performance Testing Framework
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
    echo Continuing anyway...
)

echo.
echo [2/4] Checking Ollama status...
echo NOTE: Ollama is required for AI grading tests
echo If Ollama is not running, those tests will be skipped
echo.

REM Optional: Check if Ollama is running (this is informational)
curl -s http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama does not appear to be running on localhost:11434
    echo AI grading tests may fail
    echo To start Ollama: Open a new terminal and run "ollama serve"
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        echo Exiting...
        pause
        exit /b 0
    )
) else (
    echo SUCCESS: Ollama is running
)

echo.
echo [3/4] Running comprehensive tests...
echo This may take several minutes...
echo.

python run_all_tests.py

if errorlevel 1 (
    echo.
    echo ERROR: Testing failed
    pause
    exit /b 1
)

echo.
echo [4/4] Opening HTML report...

REM Open the HTML report in default browser
if exist "results\summary_report.html" (
    start results\summary_report.html
) else (
    echo WARNING: HTML report not found
)

echo.
echo ============================================================
echo Testing Complete!
echo ============================================================
echo.
echo Generated Reports:
echo   - results\accuracy_report.json
echo   - results\performance_report.json
echo   - results\summary_report.html
echo.

pause
