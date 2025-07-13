# Bluetooth Connection: Termux Android ↔ MacBook

## 🔄 Koneksi Bluetooth Termux-MacBook

### ⚠️ Realitas Bluetooth di Termux
- Termux memiliki keterbatasan akses Bluetooth
- Android membatasi akses Bluetooth langsung untuk apps
- Bluetooth LE (Low Energy) lebih mudah daripada Classic Bluetooth

### 🛠 Setup Bluetooth di MacBook

1. **Pastikan Bluetooth aktif:**
   ```bash
   # Cek status Bluetooth
   system_profiler SPBluetoothDataType
   
   # Atau di System Preferences > Bluetooth
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
