# Universal Bluetooth Chat Guide
# Support: macOS, Windows, Linux

## 🔵 Bluetooth Connection Setup

### ⚙️ Prerequisites
- Python 3.7+
- Bluetooth adapter on both devices
- Admin/sudo access for Bluetooth operations

### � Platform Support
- ✅ **macOS** - Full support
- ✅ **Windows** - Full support  
- ✅ **Linux** - Full support

## 🛠 Step 1: Install Dependencies

### macOS:
```bash
# Install Bluetooth libraries
pip install bleak

# Check Bluetooth status
system_profiler SPBluetoothDataType | grep "State"
```

### Windows:
```bash
# Install dependencies
pip install bleak

# Check Bluetooth in Device Manager
# Control Panel > Device Manager > Bluetooth
```

### Linux:
```bash
# Install Bluetooth tools
sudo apt install bluetooth bluez-utils

# Install Python libraries
pip install bleak pybluez

# Check Bluetooth service
sudo systemctl status bluetooth
```

## 🔍 Step 2: Find Your Device ID

### Method 1: Using Built-in Tools

**macOS:**
```bash
# List Bluetooth devices
system_profiler SPBluetoothDataType

# Get your Mac's Bluetooth address
system_profiler SPBluetoothDataType | grep "Address"
```

**Windows:**
```bash
# PowerShell command
Get-PnpDevice -Class Bluetooth

# Or check in Settings > Devices > Bluetooth
```

**Linux:**
```bash
# List Bluetooth adapters
hciconfig

# Scan for devices
hcitool scan

# Get local device info
bluetoothctl show
```

### Method 2: Using Our Detection Script

```bash
# Run device detection
python detect_bluetooth.py

# Output example:
# Local Device: MacBook-Pro (XX:XX:XX:XX:XX:XX)
# Available devices:
# 1. Windows-PC (YY:YY:YY:YY:YY:YY)
# 2. Linux-Laptop (ZZ:ZZ:ZZ:ZZ:ZZ:ZZ)
```

## 🚀 Step 3: Establish Connection

### Device 1 (Server):
```bash
# Start Bluetooth server
python src/main.py server bt

# Output:
# [SERVER] Bluetooth address: XX:XX:XX:XX:XX:XX
# [SERVER] Device name: MacBook-Pro
# [SERVER] Waiting for connection...
```

### Device 2 (Client):
```bash
# Start Bluetooth client
python src/main.py client bt

# Interactive selection:
# Found 3 devices:
# 1. MacBook-Pro (XX:XX:XX:XX:XX:XX) [Server ready]
# 2. iPhone (YY:YY:YY:YY:YY:YY)
# 3. Windows-PC (ZZ:ZZ:ZZ:ZZ:ZZ:ZZ)
# Select device number: 1
```

## 🔧 Step 4: Troubleshooting Connection Issues

### Problem: "No devices found"

**Solution:**
```bash
# Make sure Bluetooth is discoverable
# macOS: System Preferences > Bluetooth > Advanced > Discoverable
# Windows: Settings > Devices > Bluetooth > More options > Allow discovery
# Linux: bluetoothctl discoverable on
```

### Problem: "Connection refused"

**Solution:**
```bash
# Pair devices first manually
# macOS: System Preferences > Bluetooth > Pair
# Windows: Settings > Devices > Add Bluetooth device
# Linux: bluetoothctl pair XX:XX:XX:XX:XX:XX
```

### Problem: "Device ID not recognized"

**Solution:**
```bash
# Use our improved detection script
python bluetooth_helper.py --scan
python bluetooth_helper.py --info
```

## 💡 Universal Connection Tips

### 1. Enable Discoverability
- **macOS:** System Preferences > Bluetooth > Advanced
- **Windows:** Settings > Devices > Bluetooth & other devices
- **Linux:** `bluetoothctl discoverable on`

### 2. Check Bluetooth Services
- **macOS:** Built-in, always running
- **Windows:** Services.msc > Bluetooth Support Service
- **Linux:** `sudo systemctl start bluetooth`

### 3. Firewall Settings
- Allow Python through firewall
- Open Bluetooth ports (typically 1-30)

## 🎯 Example Session

### Computer A (Server):
```bash
$ python src/main.py server bt
[SERVER] Local device: Computer-A (12:34:56:78:9A:BC)
[SERVER] Starting Bluetooth server...
[SERVER] Listening for connections...
[SERVER] Connection from Computer-B (DE:F0:12:34:56:78)
> Hello from Computer A!
```

### Computer B (Client):
```bash
$ python src/main.py client bt
Scanning for devices...
Found 2 devices:
1. Computer-A (12:34:56:78:9A:BC) [Chat Server]
2. Smartphone (AB:CD:EF:12:34:56)
Select device: 1
Connected to Computer-A!
[SERVER]: Hello from Computer A!
> Hello from Computer B!
```

## 📁 File Transfer

```bash
# Send file
> /send document.pdf
[FILE] Sent: document.pdf (1.2 MB)

# Receive notification
[FILE] Receiving: document.pdf (1.2 MB)
[FILE] Saved as: received_document.pdf
```

## 🔄 Fallback to WiFi

If Bluetooth fails, use WiFi mode:

```bash
# Device 1 (Server)
python src/main.py server wifi

# Device 2 (Client)  
python src/main.py client wifi
# Enter server IP when prompted
```
   ```

2. **Make MacBook discoverable:**
   - System Preferences > Bluetooth
   - Klik "Advanced" > Check "Allow Bluetooth devices to find this Mac"

### 🤖 Setup Bluetooth di Termux Android

1. **Install dependencies:**
   ```bash
   pkg install python git bluetooth bluez-utils
   
   # Install bleak for Bluetooth LE
   pip install bleak
   ```

2. **Enable Location Services:**
   - Android Settings > Location > ON
   - Required for Bluetooth scanning

3. **Give Termux Bluetooth permissions:**
   - Android Settings > Apps > Termux > Permissions
   - Enable "Nearby devices" or "Bluetooth"

### 🔧 Cara Koneksi Bluetooth

#### Method 1: Menggunakan Aplikasi Chat (Recommended)

**MacBook (Server):**
```bash
source venv/bin/activate
python src/main.py server bt
```

**Termux Android (Client):**
```bash
# Install dependencies dulu
pip install bleak

# Jalankan client
python src/termux_chat.py client bt
```

#### Method 2: Manual Bluetooth Pairing

**Di MacBook:**
```bash
# Start Bluetooth server manual
sudo rfcomm listen /dev/rfcomm0 1
```

**Di Android (via adb jika root):**
```bash
# Scan devices
hcitool scan

# Connect ke MacBook
rfcomm connect /dev/rfcomm0 [MAC_ADDRESS] 1
```

### 🚀 Step-by-Step Guide

#### Langkah 1: Persiapan MacBook
```bash
cd TerminalChatBluetooth
source venv/bin/activate

# Pastikan bleak terinstall
pip install bleak

# Start server Bluetooth
python src/main.py server bt
```

#### Langkah 2: Persiapan Termux
```bash
# Update Termux
pkg update && pkg upgrade

# Install requirements
pkg install python git
pip install bleak

# Clone project (jika belum)
git clone <repository-url>
cd TerminalChatBluetooth

# Jalankan client
python src/termux_chat.py client bt
```

#### Langkah 3: Koneksi
1. **Di Termux:** Akan scan devices otomatis
2. **Pilih MacBook** dari daftar yang muncul
3. **Android akan prompt** permission - Allow
4. **Koneksi established** - mulai chat!

### 🐛 Troubleshooting Bluetooth

#### Error: "Bluetooth device is turned off"
```bash
# Di MacBook
sudo blueutil -p 1  # Turn on Bluetooth

# Di Termux
# Enable via Android Settings
```

#### Error: "Permission denied"
```bash
# Di Termux - berikan permission
termux-setup-storage

# Di Android Settings
# Apps > Termux > Permissions > Enable Bluetooth
```

#### Error: "No devices found"
```bash
# Di MacBook - make discoverable
# System Preferences > Bluetooth > Advanced > Allow discovery

# Di Termux - enable location
# Android Settings > Location > ON
```

#### Fallback ke WiFi jika Bluetooth gagal:
```bash
# MacBook
python src/main.py server wifi

# Termux
python src/termux_chat.py client wifi
# Masukkan IP MacBook (cek dengan ifconfig di MacBook)
```

### 💡 Tips untuk Bluetooth Termux-MacBook

1. **WiFi lebih reliable** - gunakan sebagai backup
2. **Jarak dekat** - Bluetooth bekerja dalam 10 meter
3. **Permission Android** - pastikan semua permission diberikan
4. **Battery optimization** - disable untuk Termux di Android
5. **Test connection** - coba pair devices dulu via Settings

### 🔍 Debug Commands

**Di MacBook:**
```bash
# Cek Bluetooth status
system_profiler SPBluetoothDataType | grep "State"

# List paired devices
blueutil --paired

# Make discoverable
sudo discoverable on
```

**Di Termux:**
```bash
# Test Python Bluetooth
python -c "import bleak; print('Bluetooth available')"

# Check permissions
ls -la /dev/bluetooth* 2>/dev/null || echo "No Bluetooth access"
```

### ⚡ Quick Test

**MacBook Terminal 1:**
```bash
python src/main.py server bt
```

**Termux Terminal:**
```bash
python src/termux_chat.py client bt
# Pilih MacBook dari daftar
# Tunggu connection established
# Mulai chat!
```

### 🎯 Expected Output

**MacBook:**
```
[SERVER] Starting Bluetooth LE server...
[SERVER] Advertising service for clients to connect...
[SERVER] Client connected from Android device
> Hello from MacBook!
```

**Termux:**
```
🤖 Detected: Running on Termux Android
Scanning for Bluetooth devices...
Found 3 devices:
1. MacBook Pro (XX:XX:XX:XX:XX:XX)
2. iPhone (YY:YY:YY:YY:YY:YY)
Select device number: 1
Connected to MacBook Pro!
> Hello from Android Termux!
```
