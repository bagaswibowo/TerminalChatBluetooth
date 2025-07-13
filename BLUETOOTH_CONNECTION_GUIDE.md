# 🎯 PANDUAN LENGKAP: Bluetooth Connection

## ❓ Problem: "Tidak tahu device ID dan mana yang server/client"

### 🔍 Step 1: Identify Your Devices

**Sebelum mulai, run command ini di kedua perangkat:**

```bash
# Cek device info
python detect_bluetooth.py --info

# Scan devices yang tersedia
python detect_bluetooth.py --scan
```

**Example Output:**
```
🔵 Platform: Darwin
📱 Local Device Address: XX:XX:XX:XX:XX:XX

Found devices:
1. MacBook-Pro (12:34:56:78:9A:BC) 💻 Computer
2. Windows-PC (AB:CD:EF:12:34:56) 💻 Computer  
3. iPhone (98:76:54:32:10:FE) 📱 Mobile
```

### 🎯 Step 2: Decide Server vs Client

**Rule of thumb:**
- **Server** = Device yang akan "menunggu" koneksi
- **Client** = Device yang akan "mencari dan connect"

**Recommended setup:**
- 💻 **Desktop/Laptop** → Server (lebih stabil)
- 📱 **Mobile/Portable** → Client

### 🚀 Step 3: Start Connection

#### Computer A (Server):
```bash
python src/main.py server bt

# You'll see:
# 📱 Local Device: MacBook-Pro
# 🆔 Device Address: 12:34:56:78:9A:BC
# ✅ Server ready! Clients should see:
#    Device: MacBook-Pro
#    Address: 12:34:56:78:9A:BC
#    Type: Chat Server
```

#### Computer B (Client):
```bash
python src/main.py client bt

# You'll see:
# Found 3 devices:
# 1. MacBook-Pro
#    🆔 Address: 12:34:56:78:9A:BC
#    💻 Device Type: Computer (Good for chat)
#    ────────────────────────────────────
# 2. Windows-PC
#    🆔 Address: AB:CD:EF:12:34:56
#    💻 Device Type: Computer (Good for chat)
#    ────────────────────────────────────

# Select device number: 1
```

### 🔧 Step 4: Troubleshooting Connection

#### Problem: "No devices found"

**Check discoverability:**

**macOS:**
```bash
# Make discoverable via GUI
# System Preferences > Bluetooth > Advanced
# ✅ "Allow Bluetooth devices to find this Mac"

# Or via command line
sudo discoverable on
```

**Windows:**
```bash
# Settings > Devices > Bluetooth & other devices
# ✅ "Allow Bluetooth devices to find this PC"
```

**Linux:**
```bash
# Make discoverable
bluetoothctl discoverable on
bluetoothctl pairable on

# Check status
bluetoothctl show
```

#### Problem: "Connection failed"

**Try manual pairing first:**

1. **Pair devices through OS settings:**
   - macOS: System Preferences > Bluetooth > Connect
   - Windows: Settings > Add Bluetooth device
   - Linux: `bluetoothctl pair XX:XX:XX:XX:XX:XX`

2. **Then run chat application:**
   ```bash
   # Server
   python src/main.py server bt
   
   # Client  
   python src/main.py client bt
   ```

#### Problem: "Permission denied"

**Grant Bluetooth permissions:**

**macOS:**
```bash
# System Preferences > Security & Privacy > Bluetooth
# Allow Terminal/Python to use Bluetooth
```

**Linux:**
```bash
# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER
sudo systemctl restart bluetooth

# Or run with sudo
sudo python src/main.py server bt
```

### 🔄 Alternative: WiFi Mode (Always Works)

If Bluetooth keeps failing:

```bash
# Device 1 (Server)
python src/main.py server wifi
# Note the IP address shown

# Device 2 (Client)
python src/main.py client wifi
# Enter the IP address from server
```

### 💡 Quick Reference Commands

```bash
# Detect your device
python detect_bluetooth.py --info

# Scan nearby devices  
python detect_bluetooth.py --scan

# Check Bluetooth status
python detect_bluetooth.py --status

# Start Bluetooth server
python src/main.py server bt

# Start Bluetooth client
python src/main.py client bt

# WiFi fallback (server)
python src/main.py server wifi

# WiFi fallback (client)
python src/main.py client wifi
```

### 🎯 Success Indicators

**✅ Working Connection:**
```
# Server shows:
[SERVER] Client connected from XX:XX:XX:XX:XX:XX
> Hello from server!

# Client shows:  
Connected to MacBook-Pro!
[SERVER]: Hello from server!
> Hello from client!
```

**❌ Connection Issues:**
- Devices not found in scan
- "Connection refused" errors
- "Permission denied" messages
- Timeout during connection

**🔄 Use WiFi mode if these persist!**

### 📞 Quick Help

**Can't find devices?**
```bash
python detect_bluetooth.py --scan
```

**Don't know which is server/client?**
- Larger/stationary device = Server
- Smaller/mobile device = Client

**Connection keeps failing?**
```bash
python src/main.py server wifi  # Much more reliable!
```
