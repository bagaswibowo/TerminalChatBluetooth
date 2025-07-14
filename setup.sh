#!/bin/bash

# Setup script untuk Bluetooth Chat Application
# Mendukung Linux dan Windows
# Author: Terminal Chat Bluetooth

echo "🔧 Setting up Bluetooth Chat Application..."
echo

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Silakan install Python3 terlebih dahulu."
    exit 1
fi

echo "✅ Python3 ditemukan: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak ditemukan. Silakan install pip3 terlebih dahulu."
    exit 1
fi

echo "✅ pip3 ditemukan"

# Install dependencies
echo "📦 Installing dependencies..."

# Check OS and install system dependencies for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux - checking system dependencies..."
    
    # Check if we have apt (Debian/Ubuntu)
    if command -v apt-get &> /dev/null; then
        echo "Installing system dependencies with apt..."
        sudo apt-get update
        sudo apt-get install -y python3-dev libbluetooth-dev
    # Check if we have yum (RHEL/CentOS)
    elif command -v yum &> /dev/null; then
        echo "Installing system dependencies with yum..."
        sudo yum install -y python3-devel bluez-libs-devel
    # Check if we have pacman (Arch)
    elif command -v pacman &> /dev/null; then
        echo "Installing system dependencies with pacman..."
        sudo pacman -S --noconfirm python bluez bluez-libs
    else
        echo "⚠️  Unknown Linux distribution. Please install python3-dev and libbluetooth-dev manually."
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "🪟 Detected Windows - no additional system dependencies needed"
else
    echo "⚠️  Unsupported OS: $OSTYPE"
    echo "This application is designed for Linux and Windows only."
fi

# Install Python packages
pip3 install -r requirements.txt

# Check installation
echo
echo "🔍 Checking installations..."

python3 -c "import bluetooth; print('✅ PyBluez installed successfully')" 2>/dev/null || echo "❌ PyBluez installation failed"
python3 -c "import colorama; print('✅ Colorama installed successfully')" 2>/dev/null || echo "❌ Colorama installation failed"

# Create downloads directory
mkdir -p downloads
echo "✅ Downloads directory created"

# Make scripts executable
chmod +x main.py
chmod +x server.py  
chmod +x client.py
echo "✅ Scripts made executable"

echo
echo "🎉 Setup completed!"
echo
echo "📖 Usage:"
echo "  ./run.sh           # Run launcher"
echo "  python3 main.py    # Run main launcher"
echo "  python3 server.py  # Run as server"
echo "  python3 client.py  # Run as client"
echo
echo "📝 Note: Pastikan Bluetooth sudah aktif di perangkat Anda!"
