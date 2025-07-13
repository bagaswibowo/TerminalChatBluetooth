# Setup Guide untuk Termux Android

## 📱 Panduan Instalasi di Termux Android

### 1. Install Termux
Download Termux dari:
- **F-Droid** (recommended): https://f-droid.org/packages/com.termux/
- **GitHub Releases**: https://github.com/termux/termux-app/releases

⚠️ **Jangan install dari Google Play Store** (versi lama dan tidak update)

### 2. Setup Termux Environment
```bash
# Update package repository
pkg update && pkg upgrade

# Install Python dan Git
pkg install python git

# Install dependencies untuk networking
pkg install openssl libffi

# Optional: Install bluetooth tools (experimental)
pkg install bluetooth
```

### 3. Clone dan Setup Aplikasi
```bash
# Clone repository (ganti dengan URL yang benar)
git clone https://github.com/yourusername/TerminalChatBluetooth.git
cd TerminalChatBluetooth

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

#### Mode WiFi (Recommended untuk Termux)
```bash
# Sebagai server
python src/main.py server wifi

# Sebagai client (dari Termux lain atau perangkat lain)
python src/main.py client wifi
```

#### Mode Bluetooth (Experimental)
```bash
# Sebagai server
python src/main.py server bt

# Sebagai client
python src/main.py client bt
```

## 🔧 Tips untuk Termux

### Mendapatkan IP Address di Termux:
```bash
# Cek IP address
ifconfig
# atau
ip addr show
```

### Permission untuk Bluetooth di Android:
- Buka **Settings > Apps > Termux > Permissions**
- Aktifkan **Nearby devices** atau **Bluetooth**

### Storage Permission (untuk transfer file):
```bash
# Berikan akses storage
termux-setup-storage
```

## 🌐 Contoh Penggunaan Real

### Scenario 1: Android ke Android
**Termux 1 (Server):**
```bash
python src/main.py server wifi
# Server berjalan di: 192.168.1.105:8888
```

**Termux 2 (Client):**
```bash
python src/main.py client wifi
# Masukkan IP: 192.168.1.105
# Port: 8888
```

### Scenario 2: Android ke MacBook
**MacBook (Server):**
```bash
python src/main.py server wifi
# Server: 192.168.1.100:8888
```

**Termux Android (Client):**
```bash
python src/main.py client wifi
# IP: 192.168.1.100
# Port: 8888
```

## ⚠️ Troubleshooting Termux

### 1. Python tidak ditemukan:
```bash
pkg install python
```

### 2. Module tidak ditemukan:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Permission denied untuk Bluetooth:
- Aktifkan Location Services di Android
- Berikan permission Bluetooth ke Termux

### 4. Network tidak connect:
- Pastikan kedua perangkat di WiFi yang sama
- Cek firewall/security apps di Android

### 5. File transfer tidak jalan:
```bash
# Setup storage access
termux-setup-storage
# File akan tersimpan di /data/data/com.termux/files/home/
```

## 🎯 Quick Test di Termux

```bash
# Install semua dalam satu command
pkg update && pkg install python git && git clone <repo-url> && cd TerminalChatBluetooth && pip install -r requirements.txt && python src/main.py server wifi
```
