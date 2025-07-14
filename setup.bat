@echo off
REM Setup script untuk Bluetooth Chat Application - Windows
REM Author: Terminal Chat Bluetooth

echo 🔧 Setting up Bluetooth Chat Application for Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python tidak ditemukan. Silakan install Python terlebih dahulu.
    echo Download dari: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python ditemukan
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip tidak ditemukan. Silakan install pip terlebih dahulu.
    pause
    exit /b 1
)

echo ✅ pip ditemukan

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check installation
echo.
echo 🔍 Checking installations...

python -c "import bluetooth; print('✅ PyBluez installed successfully')" 2>nul || echo ❌ PyBluez installation failed
python -c "import colorama; print('✅ Colorama installed successfully')" 2>nul || echo ❌ Colorama installation failed

REM Create downloads directory
if not exist downloads mkdir downloads
echo ✅ Downloads directory created

echo.
echo 🎉 Setup completed!
echo.
echo 📖 Usage:
echo   python main.py     # Run main launcher
echo   python server.py   # Run as server
echo   python client.py   # Run as client
echo.
echo 📝 Note: Pastikan Bluetooth sudah aktif di perangkat Anda!
pause
