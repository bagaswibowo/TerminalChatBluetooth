#!/bin/bash

# Run script untuk Bluetooth Chat Application
# Author: Terminal Chat Bluetooth


PYTHON_PATH="python3"

echo "🚀 Bluetooth Chat Application Launcher"
echo "======================================="
echo


echo "✅ Using Python: $PYTHON_PATH (global)"
echo

# Show menu
echo "Select mode:"
echo "1. Bluetooth Server Mode - Wait for Bluetooth client connection"
echo "2. Bluetooth Client Mode - Connect to Bluetooth server"  
echo "3. Main Launcher - Interactive menu"
echo "4. Exit"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🔵 Starting Bluetooth Server Mode..."
        "$PYTHON_PATH" server.py
        ;;
    2)
        echo "🔗 Starting Bluetooth Client Mode..."
        "$PYTHON_PATH" client.py
        ;;
    3)
        echo "🎯 Starting Main Launcher..."
        "$PYTHON_PATH" main.py
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please try again."
        ;;
esac
