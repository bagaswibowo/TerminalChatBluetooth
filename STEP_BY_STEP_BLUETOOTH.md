# 🔵 STEP-BY-STEP: Termux Android ↔ MacBook Bluetooth

## 📋 Checklist Sebelum Mulai

### ✅ MacBook:
- [ ] Bluetooth ON
- [ ] Make MacBook discoverable (System Preferences > Bluetooth > Advanced)
- [ ] Terminal ready dengan project di folder

### ✅ Android Termux:
- [ ] Termux installed dari F-Droid (bukan Google Play)
- [ ] Location Services ON di Android
- [ ] Bluetooth permission granted ke Termux
- [ ] WiFi connected (untuk download dependencies)

## 🚀 Langkah 1: Setup MacBook (Server)

```bash
# Di MacBook Terminal
cd TerminalChatBluetooth
source venv/bin/activate

# Pastikan dependencies terinstall
pip install bleak

# Test Bluetooth
python test_bluetooth.py

# Jika test OK, start server
python src/main.py server bt
```

**Output yang diharapkan:**
```
[SERVER] Starting Bluetooth LE server...
[SERVER] Advertising service for clients to connect...
[SERVER] Bluetooth server ready!
```

## 🤖 Langkah 2: Setup Termux Android (Client)

```bash
# Di Termux
# Install dependencies
pkg update && pkg install python git

# Install project
git clone <repository-url>
cd TerminalChatBluetooth

# Install Python packages
pip install bleak

# Test Bluetooth capability
python test_bluetooth.py
```

**Jika test bluetooth gagal, cek:**
1. Android Settings > Location > ON
2. Android Settings > Apps > Termux > Permissions > Allow Bluetooth
3. Android Settings > Battery > Apps > Termux > Don't optimize

## 🔗 Langkah 3: Koneksi Bluetooth

**Di Termux (Client):**
```bash
python src/termux_chat.py client bt
```

**Expected flow:**
```
🤖 Detected: Running on Termux Android
🔍 Scanning for Bluetooth devices...
⏳ Please wait 10-15 seconds...

✅ Found 3 devices:
1. MacBook Pro (XX:XX:XX:XX:XX:XX)
2. iPhone (YY:YY:YY:YY:YY:YY)
3. AirPods (ZZ:ZZ:ZZ:ZZ:ZZ:ZZ)

Select device number: 1
🔄 Testing connection to MacBook Pro...
✅ Successfully connected to MacBook Pro!
Connected to MacBook Pro!
> 
```

## 💬 Langkah 4: Mulai Chat!

**Di MacBook:**
```
> Hello from MacBook!
```

**Di Termux:**
```
[SERVER]: Hello from MacBook!
> Hello from Android Termux!
```

**Transfer file:**
```
> /send test_file.txt
[FILE] Sent: test_file.txt
```

## 🐛 Troubleshooting

### Problem 1: "No devices found"
**Solution:**
```bash
# Di MacBook - make discoverable
# System Preferences > Bluetooth > Advanced > 
# ✅ "Allow Bluetooth devices to find this Mac"

# Di Termux - check permissions
# Android Settings > Apps > Termux > Permissions
# ✅ Enable all location and bluetooth permissions
```

### Problem 2: "Bluetooth device is turned off"
**Solution:**
```bash
# Android: Settings > Connected devices > Bluetooth > ON
# MacBook: System Preferences > Bluetooth > Turn On
```

### Problem 3: "Connection failed"
**Solution:**
```bash
# Try pairing devices manually first:
# Android Settings > Connected devices > Bluetooth > Pair new device
# Select MacBook from list

# Then try app again
python src/termux_chat.py client bt
```

### Problem 4: Permission denied
**Solution:**
```bash
# Android Settings > Privacy > Permission manager > Location
# Find Termux > Allow

# Also check:
# Settings > Apps > Termux > Permissions > Allow all
```

## 🔄 Fallback ke WiFi

Jika Bluetooth tidak bekerja, gunakan WiFi mode:

**MacBook:**
```bash
python src/main.py server wifi
# Note IP address: contoh 192.168.1.100
```

**Termux:**
```bash
python src/termux_chat.py client wifi
# Masukkan IP MacBook: 192.168.1.100
# Port: 8888
```

## 📱 Quick Commands Reference

### MacBook (Server):
```bash
# Bluetooth
python src/main.py server bt

# WiFi
python src/main.py server wifi

# Check IP
ifconfig | grep inet
```

### Termux (Client):
```bash
# Bluetooth  
python src/termux_chat.py client bt

# WiFi
python src/termux_chat.py client wifi

# Check setup
python test_bluetooth.py
```

### Chat Commands:
```bash
# Send message
> Hello world!

# Send file
> /send /path/to/file.txt

# Quit
> /quit
```

## ⚡ Pro Tips

1. **Start dengan WiFi** untuk test koneksi basic
2. **Pair devices manually** di Android Settings dulu
3. **Jarak dekat** - dalam 5 meter untuk Bluetooth
4. **Restart Bluetooth** jika scanning gagal
5. **Check battery optimization** - disable untuk Termux
6. **Use latest Termux** dari F-Droid

## 🎯 Success Indicators

✅ **Bluetooth Working:**
- Device scanning finds MacBook
- Connection established without errors
- Messages appear real-time
- File transfer works

❌ **Use WiFi Instead:**
- Scanning always fails
- Permission errors persist  
- Connection timeouts
- Android restrictions too strict
