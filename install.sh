#!/bin/bash
# Install script for macOS and Linux

echo "=== Terminal Chat Bluetooth Installer ==="
echo "Installing dependencies for macOS/Linux..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Platform-specific instructions
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    echo "Note: You may need to enable Bluetooth permissions for Terminal in System Preferences > Security & Privacy > Privacy > Bluetooth"
    
    # Check if Homebrew is available for system dependencies
    if command -v brew &> /dev/null; then
        echo "Installing system dependencies with Homebrew..."
        brew install pkg-config
    else
        echo "Warning: Homebrew not found. You may need to install pkg-config manually if you encounter build errors."
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    echo "Installing system dependencies..."
    
    # Detect package manager and install dependencies
    if command -v apt-get &> /dev/null; then
        echo "Using apt-get..."
        sudo apt-get update
        sudo apt-get install -y python3-dev libbluetooth-dev pkg-config
    elif command -v yum &> /dev/null; then
        echo "Using yum..."
        sudo yum install -y python3-devel bluez-libs-devel pkgconfig
    elif command -v pacman &> /dev/null; then
        echo "Using pacman..."
        sudo pacman -S python bluez-libs pkg-config
    else
        echo "Warning: Could not detect package manager. Please install python3-dev, libbluetooth-dev, and pkg-config manually."
    fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Try alternative pybluez installation if the first fails
if ! python3 -c "import bluetooth" 2>/dev/null; then
    echo "Standard pybluez installation failed. Trying alternative..."
    pip3 install --user git+https://github.com/pybluez/pybluez.git
fi

# Make the script executable
chmod +x bluetooth_chat.py

echo ""
echo "=== Installation Complete ==="
echo "To run the application:"
echo "  python3 bluetooth_chat.py"
echo ""
echo "Note: Make sure Bluetooth is enabled on your device."
echo "On Linux, you may need to run with sudo for Bluetooth access."
