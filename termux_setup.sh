#!/bin/bash
# Auto setup script untuk Termux Android

echo "🤖 Terminal Chat - Termux Setup Script"
echo "======================================="

# Check if running on Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ Error: Script ini hanya untuk Termux Android"
    exit 1
fi

echo "✅ Detected: Running on Termux Android"
echo ""

# Update packages
echo "📦 Updating Termux packages..."
pkg update -y
pkg upgrade -y

# Install required packages
echo "🔧 Installing Python and Git..."
pkg install python git openssl libffi -y

# Setup storage access
echo "💾 Setting up storage access..."
termux-setup-storage

# Clone repository (user will need to provide the actual URL)
echo "📥 Ready to clone repository..."
echo "Please run manually:"
echo "git clone <your-repository-url>"
echo "cd TerminalChatBluetooth"
echo ""

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip

# Create a simple requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "bleak>=1.0.0" > requirements.txt
fi

pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "python src/termux_chat.py server wifi"
echo ""
echo "📱 Tips:"
echo "- Use 'ifconfig' to find your IP address"
echo "- Use WiFi mode for best compatibility"
echo "- Connect from other devices using your Termux IP"
