@echo off
REM UEFA Mobile Auto-Processor Service
REM Run this to start the background service

echo ================================
echo UEFA Mobile Auto-Processor
echo ================================
echo.

REM Change to the script directory
cd /d "%~dp0"

echo Starting auto-processor service...
echo Press Ctrl+C to stop the service
echo.

REM Run the auto-processor
python mobile_auto_processor.py start

echo.
echo Service stopped.
pause