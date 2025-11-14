@echo off
echo 🕰️ Creating UEFA Mobile Auto-Processor Scheduled Task...
echo.

REM Create the scheduled task
schtasks /create /tn "UEFA_Mobile_Auto_Processor" /tr "python \"%~dp0mobile_auto_processor.py\" once" /sc hourly /st 12:00 /sd 11/14/2025 /ru "%USERNAME%" /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo ✅ Successfully created scheduled task!
    echo.
    echo 📅 Task will run every hour starting at 12:00 PM
    echo 🔄 Processing mobile UEFA results automatically
    echo.
    echo Task Management:
    echo   View:   schtasks /query /tn "UEFA_Mobile_Auto_Processor"
    echo   Run:    schtasks /run /tn "UEFA_Mobile_Auto_Processor" 
    echo   Delete: schtasks /delete /tn "UEFA_Mobile_Auto_Processor" /f
    echo.
    pause
) else (
    echo ❌ Failed to create scheduled task
    echo You may need to run this as Administrator
    echo.
    pause
)