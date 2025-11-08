#!/bin/bash
# AutoGradePro Performance Testing Setup and Runner
# Linux/Mac Bash Script

echo "============================================================"
echo "AutoGradePro Performance Testing Framework"
echo "============================================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "WARNING: Some dependencies may not have installed correctly"
    echo "Continuing anyway..."
fi

echo
echo "[2/4] Checking Ollama status..."
echo "NOTE: Ollama is required for AI grading tests"
echo

# Check if Ollama is running
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "SUCCESS: Ollama is running"
else
    echo "WARNING: Ollama does not appear to be running"
    echo "To start Ollama: Open a new terminal and run 'ollama serve'"
    echo
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo "Exiting..."
        exit 0
    fi
fi

echo
echo "[3/4] Running comprehensive tests..."
echo "This may take several minutes..."
echo

python3 run_all_tests.py

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Testing failed"
    exit 1
fi

echo
echo "[4/4] Opening HTML report..."

# Open the HTML report
if [ -f "results/summary_report.html" ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open results/summary_report.html
    elif command -v open &> /dev/null; then
        open results/summary_report.html
    else
        echo "Please open results/summary_report.html manually"
    fi
else
    echo "WARNING: HTML report not found"
fi

echo
echo "============================================================"
echo "Testing Complete!"
echo "============================================================"
echo
echo "Generated Reports:"
echo "  - results/accuracy_report.json"
echo "  - results/performance_report.json"
echo "  - results/summary_report.html"
echo
