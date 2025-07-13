#!/bin/bash
# Install script for Termux (Android)

echo "=== Terminal Chat Bluetooth Installer for Termux ==="
echo "Installing dependencies for Termux (Android)..."

# Update packages
echo "Updating package list..."
pkg update -y

# Install required packages
echo "Installing required packages..."
pkg install -y python python-dev clang make pkg-config bluetooth-dev

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Try alternative installations if needed
if ! python -c "import bluetooth" 2>/dev/null; then
    echo "Trying alternative pybluez installation..."
    pip install git+https://github.com/pybluez/pybluez.git
fi

# Make the script executable
chmod +x bluetooth_chat.py

echo ""
echo "=== Installation Complete ==="
echo "To run the application:"
echo "  python bluetooth_chat.py"
echo ""
echo "IMPORTANT NOTES FOR TERMUX:"
echo "1. Make sure Bluetooth is enabled on your Android device"
echo "2. Grant location permissions to Termux (required for Bluetooth scanning)"
echo "3. Some Android versions may require additional permissions"
echo "4. You may need to pair devices first in Android Settings"
echo ""
echo "If you encounter permission errors, try:"
echo "  termux-setup-storage"
echo "  (This grants Termux access to storage)"
