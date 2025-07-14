@echo off
REM Run script untuk Bluetooth Chat Application - Windows
REM Author: Terminal Chat Bluetooth

echo 🚀 Bluetooth Chat Application Launcher
echo =======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Using Python
python --version
echo.

REM Show menu
echo Select mode:
echo 1. Bluetooth Server Mode - Wait for Bluetooth client connection
echo 2. Bluetooth Client Mode - Connect to Bluetooth server
echo 3. Main Launcher - Interactive menu
echo 4. Exit
echo.

set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" (
    echo 🔵 Starting Bluetooth Server Mode...
    python server.py
) else if "%choice%"=="2" (
    echo 🔗 Starting Bluetooth Client Mode...
    python client.py
) else if "%choice%"=="3" (
    echo 🎯 Starting Main Launcher...
    python main.py
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice. Please try again.
    pause
    goto :eof
)

pause
