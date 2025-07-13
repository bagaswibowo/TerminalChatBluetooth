@echo off
REM Install script for Windows

echo === Terminal Chat Bluetooth Installer ===
echo Installing dependencies for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH. Please install Python 3 first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install -r requirements.txt

REM For Windows, we might need to install pybluez from wheel
echo.
echo Note: If pybluez installation fails, you may need to:
echo 1. Install Microsoft Visual C++ Build Tools
echo 2. Or use a pre-compiled wheel from:
echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pybluez

echo.
echo === Installation Complete ===
echo To run the application:
echo   python bluetooth_chat.py
echo.
echo Note: Make sure Bluetooth is enabled on your device.
echo You may need to pair devices first in Windows Settings.
pause
