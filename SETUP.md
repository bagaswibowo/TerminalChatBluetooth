# Terminal Chat Bluetooth - Setup Guide

## Quick Start

### 1. Installation
Choose the installation method for your platform:

**macOS/Linux:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

**Termux (Android):**
```bash
./install_termux.sh
```

### 2. Running
```bash
python3 launcher.py
```
The launcher will automatically detect if Bluetooth is available and choose the appropriate version.

## Platform-Specific Setup

### macOS
1. Enable Bluetooth in System Preferences
2. Grant Terminal access to Bluetooth:
   - System Preferences → Security & Privacy → Privacy → Bluetooth
   - Add Terminal.app
3. If using iTerm2, add it to the Bluetooth permissions as well

### Windows
1. Enable Bluetooth in Settings
2. Install Microsoft Visual C++ Build Tools if you encounter compilation errors
3. Some Windows versions may require administrator privileges

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev libbluetooth-dev pkg-config

# Add user to bluetooth group (optional, to avoid sudo)
sudo usermod -a -G bluetooth $USER
# Log out and log back in for changes to take effect

# Enable Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

### Linux (CentOS/RHEL)
```bash
# Install system dependencies
sudo yum install python3-devel bluez-libs-devel pkgconfig

# Enable Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

### Linux (Arch)
```bash
# Install system dependencies
sudo pacman -S python bluez-libs pkg-config

# Enable Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

### Termux (Android)
1. Install Termux from F-Droid (not Google Play Store)
2. Grant storage permissions:
   ```bash
   termux-setup-storage
   ```
3. Grant location permissions to Termux in Android Settings
4. Enable Bluetooth on your Android device

## Testing the Installation

### Test 1: Basic functionality
```bash
python3 -c "
try:
    import bluetooth
    print('✅ PyBluez available')
except ImportError:
    print('⚠️ PyBluez not available, will use TCP fallback')

try:
    import colorama
    print('✅ Colorama available')
except ImportError:
    print('⚠️ Colorama not available, using basic colors')

try:
    import tqdm
    print('✅ tqdm available')
except ImportError:
    print('⚠️ tqdm not available, using basic progress')
"
```

### Test 2: Bluetooth detection
```bash
python3 -c "
import bluetooth
try:
    devices = bluetooth.discover_devices()
    print(f'✅ Bluetooth working, found {len(devices)} devices')
except Exception as e:
    print(f'❌ Bluetooth error: {e}')
"
```

### Test 3: Two-device setup
1. On Device A: `python3 launcher.py` → Choose "Start server"
2. On Device B: `python3 launcher.py` → Choose "Connect to device"

## Troubleshooting Common Issues

### Issue: "No module named 'bluetooth'"
**Solution:**
```bash
pip install pybluez
# If that fails, try:
pip install git+https://github.com/pybluez/pybluez.git
```

### Issue: "Permission denied" on Linux
**Solutions:**
1. Run with sudo: `sudo python3 launcher.py`
2. Or add user to bluetooth group:
   ```bash
   sudo usermod -a -G bluetooth $USER
   # Then log out and back in
   ```

### Issue: "Bluetooth not found" on Windows
**Solutions:**
1. Install Microsoft Visual C++ Build Tools
2. Download pre-compiled wheel:
   ```cmd
   pip install --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/#pybluez pybluez
   ```

### Issue: Can't find devices
**Solutions:**
1. Ensure Bluetooth is enabled on both devices
2. Make devices discoverable
3. Reduce distance between devices
4. On Android, grant location permissions to Termux

### Issue: Connection drops frequently
**Solutions:**
1. Keep devices within 5-10 meters
2. Avoid interference (WiFi routers, other Bluetooth devices)
3. Ensure devices are not going to sleep
4. On mobile devices, disable power saving for the terminal app

### Issue: File transfer fails
**Solutions:**
1. Check available storage space
2. Try smaller files first
3. Ensure downloads directory is writable
4. Check file permissions

## Performance Tips

1. **File Transfer**: Files under 10MB transfer most reliably
2. **Connection Stability**: Keep devices stationary during transfer
3. **Battery**: Bluetooth usage will drain battery on mobile devices
4. **Memory**: Large files are processed in chunks to minimize memory usage

## Advanced Configuration

Edit `config.json` to customize:
- Bluetooth port and scan duration
- File transfer settings
- UI preferences
- Security options

## Security Considerations

- Bluetooth connections use standard Bluetooth encryption
- Files are transferred directly between devices (no cloud storage)
- Connection logs are stored locally only
- No internet connection required or used

## Getting Help

1. Check this setup guide
2. Review the main README.md
3. Test with the TCP fallback version first
4. Check system Bluetooth settings
5. Verify permissions and dependencies
