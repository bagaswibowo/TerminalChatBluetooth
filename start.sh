#!/bin/bash
# Quick start script for Terminal Chat Bluetooth

set -e

echo "🚀 Terminal Chat Bluetooth - Quick Start"
echo "========================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

# Check if this is the first run
if [ ! -f ".setup_complete" ]; then
    echo "🔧 First time setup detected..."
    
    # Run installation
    if [ -f "Makefile" ]; then
        echo "📦 Running installation..."
        make install
    else
        echo "📦 Running basic installation..."
        if [ "$(uname)" = "Darwin" ] || [ "$(uname)" = "Linux" ]; then
            chmod +x install.sh
            ./install.sh
        else
            echo "Please run install.bat on Windows"
            exit 1
        fi
    fi
    
    # Run tests
    echo "🧪 Running system tests..."
    python3 test.py
    
    # Mark setup as complete
    touch .setup_complete
    echo "✅ Setup complete!"
    echo ""
fi

# Ask user what they want to do
echo "What would you like to do?"
echo "1. Start chat (auto-detect best version)"
echo "2. Run Bluetooth chat (force Bluetooth)"
echo "3. Run TCP chat (for testing/fallback)"
echo "4. Test system"
echo "5. Scan for Bluetooth devices"
echo "6. Show help"
echo "7. Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo "🎯 Starting chat with auto-detection..."
        python3 launcher.py
        ;;
    2)
        echo "📡 Starting Bluetooth chat..."
        python3 bluetooth_chat.py
        ;;
    3)
        echo "🌐 Starting TCP chat..."
        python3 tcp_chat_fallback.py
        ;;
    4)
        echo "🧪 Running system tests..."
        python3 test.py
        ;;
    5)
        echo "🔍 Scanning for Bluetooth devices..."
        python3 test.py --scan
        ;;
    6)
        echo "📚 Showing help..."
        cat << 'EOF'

Terminal Chat Bluetooth - Help
=============================

QUICK START:
1. Make sure Bluetooth is enabled on both devices
2. Run this script on both devices
3. On first device: Choose "Start chat" then "Start server"
4. On second device: Choose "Start chat" then "Connect to device"
5. Select the first device from the list
6. Start chatting!

COMMANDS IN CHAT:
/file <path>  - Send a file
/history      - Show chat history
/quit         - Exit chat
/help         - Show help

TROUBLESHOOTING:
- If Bluetooth doesn't work, try the TCP fallback option
- On Linux, you may need to run with sudo
- Make sure devices are within 10 meters of each other
- Check that Bluetooth permissions are granted

For detailed setup instructions, see SETUP.md
For full documentation, see README.md

EOF
        ;;
    7)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
