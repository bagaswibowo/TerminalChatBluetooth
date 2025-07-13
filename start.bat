@echo off
REM Quick start script for Terminal Chat Bluetooth on Windows

echo 🚀 Terminal Chat Bluetooth - Quick Start
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3 first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if this is the first run
if not exist ".setup_complete" (
    echo 🔧 First time setup detected...
    
    echo 📦 Running installation...
    call install.bat
    if %errorlevel% neq 0 (
        echo ❌ Installation failed
        pause
        exit /b 1
    )
    
    echo 🧪 Running system tests...
    python test.py
    
    REM Mark setup as complete
    echo. > .setup_complete
    echo ✅ Setup complete!
    echo.
)

:menu
echo What would you like to do?
echo 1. Start chat (auto-detect best version)
echo 2. Run Bluetooth chat (force Bluetooth)
echo 3. Run TCP chat (for testing/fallback)
echo 4. Test system
echo 5. Scan for Bluetooth devices
echo 6. Show help
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo 🎯 Starting chat with auto-detection...
    python launcher.py
    goto end
)

if "%choice%"=="2" (
    echo 📡 Starting Bluetooth chat...
    python bluetooth_chat.py
    goto end
)

if "%choice%"=="3" (
    echo 🌐 Starting TCP chat...
    python tcp_chat_fallback.py
    goto end
)

if "%choice%"=="4" (
    echo 🧪 Running system tests...
    python test.py
    goto menu
)

if "%choice%"=="5" (
    echo 🔍 Scanning for Bluetooth devices...
    python test.py --scan
    goto menu
)

if "%choice%"=="6" (
    echo 📚 Showing help...
    echo.
    echo Terminal Chat Bluetooth - Help
    echo =============================
    echo.
    echo QUICK START:
    echo 1. Make sure Bluetooth is enabled on both devices
    echo 2. Run this script on both devices
    echo 3. On first device: Choose "Start chat" then "Start server"
    echo 4. On second device: Choose "Start chat" then "Connect to device"
    echo 5. Select the first device from the list
    echo 6. Start chatting!
    echo.
    echo COMMANDS IN CHAT:
    echo /file ^<path^>  - Send a file
    echo /history      - Show chat history
    echo /quit         - Exit chat
    echo /help         - Show help
    echo.
    echo TROUBLESHOOTING:
    echo - If Bluetooth doesn't work, try the TCP fallback option
    echo - Make sure devices are within 10 meters of each other
    echo - Check that Bluetooth is enabled and drivers are installed
    echo - You may need to pair devices first in Windows Settings
    echo.
    echo For detailed setup instructions, see SETUP.md
    echo For full documentation, see README.md
    echo.
    pause
    goto menu
)

if "%choice%"=="7" (
    echo 👋 Goodbye!
    goto end
)

echo ❌ Invalid choice. Please try again.
goto menu

:end
pause
