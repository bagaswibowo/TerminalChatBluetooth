# Terminal Chat Application

Aplikasi chat terminal yang mendukung komunikasi dan transfer file melalui **WiFi** atau **Bluetooth**.

## 🚀 Fitur
- ✅ **Chat real-time** antar perangkat
- ✅ **Transfer file** dengan perintah `/send`
- ✅ **Dua mode koneksi**: WiFi dan Bluetooth
- ✅ **Cross-platform**: macOS, Windows, Linux, Android (Termux)
- ✅ **Tanpa setup kompleks**

## 📱 Platform yang Didukung
- ✅ **macOS**
- ✅ **Windows**  
- ✅ **Linux**
- ✅ **Android (via Termux)** ⭐

## 🤖 Khusus untuk Termux Android

### Quick Setup Termux:
```bash
# Install Termux dari F-Droid (bukan Google Play!)
# Jalankan di Termux:
pkg update && pkg install python git
git clone <repository_url>
cd TerminalChatBluetooth
pip install -r requirements.txt

# Gunakan script khusus Termux:
python src/termux_chat.py server wifi
```

### 💡 Tips Termux:
- **File access:** Jalankan `termux-setup-storage` untuk akses file
- **IP Address:** Gunakan `ifconfig` untuk cek IP
- **Recommended:** Gunakan mode WiFi (lebih stabil di Android)
- **File location:** File tersimpan di `~/received_<filename>`

## 🛠 Instalasi

1. **Clone repository:**
   ```bash
   git clone <repository_url>
   cd TerminalChatBluetooth
   ```

2. **Setup virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Cara Menggunakan

### Mode 1: WiFi/TCP (Recommended)

**Terminal 1 (Server):**
```bash
python src/main.py server wifi
```

**Terminal 2 (Client):**
```bash
python src/main.py client wifi
# Masukkan IP server dan port (default: localhost:8888)
```

### Mode 2: Bluetooth (Experimental)

**⚠️ Pastikan Bluetooth aktif di kedua perangkat**

#### 🔵 Termux Android ↔ MacBook:
**MacBook (Server):**
```bash
python src/main.py server bt
```

**Termux Android (Client):**
```bash
python src/termux_chat.py client bt
# Pilih MacBook dari daftar scan
```

#### 🔧 Setup Requirements:
- **Android:** Location Services ON, Bluetooth permission untuk Termux
- **MacBook:** Bluetooth ON, set discoverable
- **Jarak:** Dalam 10 meter
- **Fallback:** Gunakan WiFi jika Bluetooth gagal

📖 **Panduan lengkap:** `STEP_BY_STEP_BLUETOOTH.md`

## 📡 Koneksi Antar Perangkat Berbeda

### WiFi Mode:
1. **Cari IP server:** `ifconfig` (macOS/Linux) atau `ipconfig` (Windows)
2. **Di client:** masukkan IP tersebut

### Bluetooth Mode:
1. **Pastikan Bluetooth aktif** di kedua perangkat
2. **Perangkat harus discoverable**
3. **Client akan scan dan tampilkan daftar perangkat**

## 💬 Perintah Chat

- **Chat biasa:** Ketik pesan dan tekan Enter
- **Kirim file:** `/send /path/to/file.txt`
- **Keluar:** `/quit`

## 📖 Contoh Penggunaan

### WiFi Mode:
```bash
# Terminal 1 (MacBook)
$ python src/main.py server wifi
[SERVER] Chat server started on localhost:8888

# Terminal 2 (Android Termux)
$ python src/main.py client wifi
Server IP: 192.168.1.100
Server Port: 8888
Connected to 192.168.1.100:8888
> Hello from Android!
```

### Bluetooth Mode:
```bash
# Terminal 1 (Server)
$ python src/main.py server bt
[SERVER] Starting Bluetooth LE server...

# Terminal 2 (Client)
$ python src/main.py client bt
Scanning for Bluetooth devices...
Found 3 devices:
1. MacBook Pro (XX:XX:XX:XX:XX:XX)
2. iPhone (YY:YY:YY:YY:YY:YY)
Select device number: 1
Connected to MacBook Pro!
```

## 🔧 Troubleshooting

### WiFi Mode:
- **Port sudah digunakan:** Ubah port default (8888)
- **Tidak bisa connect:** Periksa firewall dan jaringan
- **Permission denied:** Gunakan port > 1024

### Bluetooth Mode:
- **"Bluetooth device is turned off":** Aktifkan Bluetooth
- **Device tidak terdeteksi:** Pastikan discoverable mode aktif
- **Import error:** Install dependencies: `pip install bleak`

### Platform Specific:
- **macOS:** Berikan permission Bluetooth ke Terminal
- **Linux:** Mungkin perlu `sudo` untuk Bluetooth
- **Windows:** Install Visual C++ Build Tools jika error
- **Termux:** `pkg install python bluetooth`

## 🔒 Catatan Keamanan

- ⚠️ Komunikasi **tidak terenkripsi**
- 🔒 Gunakan hanya di jaringan yang dipercaya
- 📁 File diterima akan disimpan dengan prefix "received_"

## 🎉 Quick Start

**Untuk testing cepat (WiFi):**
```bash
# Terminal 1
python src/main.py server wifi

# Terminal 2  
python src/main.py client wifi
# Tekan Enter untuk localhost:8888
```
