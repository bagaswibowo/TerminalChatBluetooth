# Bluetooth Chat Application

Aplikasi chat dan transfer file menggunakan koneksi Bluetooth yang dapat dijalankan dari terminal.

## Fitur

- 💬 **Chat Real-time**: Mengirim dan menerima pesan secara real-time melalui Bluetooth
- 📁 **Transfer File**: Mengirim file apapun (gambar, dokumen, video, dll) melalui Bluetooth
- 🎨 **Interface Colorful**: Tampilan terminal yang menarik dengan warna-warna
- 🔍 **Device Discovery**: Otomatis mencari perangkat Bluetooth yang tersedia
- 🔒 **Koneksi Aman**: Menggunakan protokol RFCOMM Bluetooth

## Requirements

- Python 3.6+
- Linux atau Windows dengan Bluetooth support
- PyBluez library untuk akses Bluetooth
- Perangkat Bluetooth lain untuk testing

## Installation

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev libbluetooth-dev

# Install Python dependencies
pip install -r requirements.txt
```

### Windows
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Setup Otomatis
```bash
./setup.sh  # Linux
# atau
python setup.py  # Windows
```

## Quick Start

### Linux
**Terminal 1** - Server:
```bash
./run.sh
# Pilih: 1. Bluetooth Server Mode
```

**Terminal 2** - Client:
```bash
./run.sh
# Pilih: 2. Bluetooth Client Mode
```

### Windows
**Terminal 1** - Server:
```cmd
python server.py
```

**Terminal 2** - Client:
```cmd
python client.py
```

## Cara Penggunaan

### Launcher Script

Jalankan launcher utama:
```bash
./run.sh
```

Menu yang tersedia:
1. **Bluetooth Server Mode** - Server Bluetooth
2. **Bluetooth Client Mode** - Client Bluetooth  
3. **Main Launcher** - Menu interaktif
4. **Exit** - Keluar

### Perintah Chat

Setelah terhubung, gunakan perintah:

- **Chat biasa**: Ketik pesan dan tekan Enter
- **Kirim file**: `/file <path_to_file>`
  - Contoh: `/file ~/Documents/foto.jpg`
  - Contoh: `/file ./document.pdf`
- **Keluar**: `/quit`

## Contoh Penggunaan

1. **Setup Server** (Perangkat A):
   ```bash
   ./run.sh
   # Pilih: 1. Bluetooth Server Mode
   ```
   
2. **Setup Client** (Perangkat B):
   ```bash
   ./run.sh
   # Pilih: 2. Bluetooth Client Mode
   ```
   
3. **Chat**:
   ```
   Halo, apa kabar?
   ```
   
4. **Transfer file**:
   ```
   /file ~/Downloads/presentasi.pptx
   ```

## File Structure

```
TerminalChatBluetooth/
├── main.py              # Launcher utama
├── server.py            # Server Bluetooth
├── client.py            # Client Bluetooth  
├── requirements.txt     # Dependencies
├── downloads/           # Folder untuk file yang diterima
└── README.md           # Dokumentasi
```

## Troubleshooting

### Error "Import bluetooth could not be resolved"
- Pastikan PyBluez sudah terinstall: `pip3 install pybluez`
- Di macOS: `brew install boost-python3` kemudian `pip3 install pybluez`

### Error "No Bluetooth devices found"
- Pastikan Bluetooth sudah aktif di kedua perangkat
- Pastikan perangkat dalam mode discoverable
- Coba restart Bluetooth service

### Error "Permission denied" 
- Di macOS, berikan permission untuk Terminal mengakses Bluetooth
- Buka System Preferences > Security & Privacy > Privacy > Bluetooth

### Koneksi terputus terus-menerus
- Pastikan jarak antar perangkat tidak terlalu jauh (< 10 meter)
- Hindari interference dari perangkat WiFi lain
- Restart aplikasi jika perlu

## Supported File Types

Aplikasi ini mendukung transfer file apapun:
- 📄 Dokumen (PDF, DOC, TXT, dll)
- 🖼️ Gambar (JPG, PNG, GIF, dll)  
- 🎵 Audio (MP3, WAV, dll)
- 🎬 Video (MP4, AVI, dll)
- 📦 Archive (ZIP, RAR, dll)
- Dan file lainnya

## Troubleshooting

### Linux
```bash
# Jika PyBluez gagal install
sudo apt-get install python3-dev libbluetooth-dev
pip install pybluez

# Jika ada permission error
sudo usermod -a -G dialout $USER
# Logout dan login kembali
```

### Windows
```cmd
# Jika ada masalah dengan PyBluez
pip install --upgrade pip
pip install pybluez

# Pastikan Bluetooth driver terinstall
```

### Error "No Bluetooth devices found"
- Pastikan Bluetooth sudah aktif di kedua perangkat
- Pastikan perangkat dalam mode discoverable
- Coba restart Bluetooth service

### Koneksi terputus terus-menerus
- Pastikan jarak antar perangkat tidak terlalu jauh (< 10 meter)
- Hindari interference dari perangkat WiFi lain
- Restart aplikasi jika perlu
