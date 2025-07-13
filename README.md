# Terminal Chat Bluetooth

Aplikasi chat terminal lintas platform yang menggunakan koneksi Bluetooth untuk komunikasi offline dan transfer file. Mendukung macOS, Windows, Linux, dan Termux (Android).

## Fitur

- ✅ Chat real-time melalui Bluetooth
- ✅ Transfer file dengan progress indicator
- ✅ Cross-platform (macOS, Windows, Linux, Termux)
- ✅ Interface terminal yang mudah digunakan
- ✅ Riwayat chat
- ✅ Koneksi offline (tidak perlu internet)
- ✅ Auto-detection perangkat Bluetooth
- ✅ Colored output untuk pengalaman yang lebih baik

## Persyaratan Sistem

### Semua Platform
- Python 3.6 atau lebih baru
- Bluetooth adapter yang aktif
- Perangkat yang ingin dihubungkan harus dalam jangkauan Bluetooth

### macOS
- macOS 10.12 atau lebih baru
- Xcode Command Line Tools (untuk kompilasi dependencies)
- Homebrew (opsional, untuk instalasi yang lebih mudah)

### Windows
- Windows 10 atau lebih baru
- Microsoft Visual C++ Build Tools (untuk kompilasi pybluez)
- Atau pre-compiled wheel pybluez

### Linux
- Ubuntu/Debian: `python3-dev`, `libbluetooth-dev`, `pkg-config`
- CentOS/RHEL: `python3-devel`, `bluez-libs-devel`, `pkgconfig`
- Arch: `python`, `bluez-libs`, `pkg-config`

### Termux (Android)
- Android 7.0 atau lebih baru
- Termux app dari F-Droid
- Izin lokasi untuk scanning Bluetooth
- Storage permission untuk transfer file

## Instalasi

### macOS & Linux
```bash
chmod +x install.sh
./install.sh
```

### Windows
```cmd
install.bat
```

### Termux (Android)
```bash
chmod +x install_termux.sh
./install_termux.sh
```

### Manual Installation
```bash
pip install -r requirements.txt
```

## Cara Penggunaan

### Menjalankan Aplikasi
```bash
python3 bluetooth_chat.py
```

### Menu Utama
1. **Start server** - Mulai server dan tunggu koneksi dari perangkat lain
2. **Connect to device** - Scan dan hubungkan ke perangkat lain
3. **Scan for devices** - Lihat perangkat Bluetooth yang tersedia
4. **Exit** - Keluar dari aplikasi

### Perintah Chat
- `/file <path>` - Kirim file
- `/history` - Tampilkan riwayat chat
- `/quit` - Keluar dari chat
- `/help` - Tampilkan bantuan

### Contoh Penggunaan

#### Scenario 1: Dua laptop terhubung
**Laptop A (Server):**
```bash
python3 bluetooth_chat.py
# Pilih "1. Start server"
# Tunggu koneksi dari Laptop B
```

**Laptop B (Client):**
```bash
python3 bluetooth_chat.py
# Pilih "2. Connect to device"
# Pilih alamat Bluetooth Laptop A
```

#### Scenario 2: Android dan Laptop
**Android (Termux - Server):**
```bash
python bluetooth_chat.py
# Pilih "1. Start server"
```

**Laptop (Client):**
```bash
python3 bluetooth_chat.py
# Pilih "2. Connect to device"
# Pilih alamat Bluetooth Android
```

## Transfer File

### Mengirim File
```
/file /path/to/your/file.txt
```

### Lokasi Download
File yang diterima akan disimpan di:
- **macOS/Linux**: `~/Downloads/BluetoothChat/`
- **Windows**: `%USERPROFILE%\Downloads\BluetoothChat\`
- **Termux**: `~/Downloads/BluetoothChat/`

## Troubleshooting

### Error: "Bluetooth not available"
- Pastikan PyBluez terinstall dengan benar
- Di Linux, coba jalankan dengan `sudo`
- Di Windows, pastikan Visual C++ Build Tools terinstall

### Error: "Permission denied"
- **Linux**: Jalankan dengan `sudo` atau tambahkan user ke grup `bluetooth`
- **Android**: Berikan izin lokasi ke Termux
- **macOS**: Izinkan akses Bluetooth di System Preferences

### Error: "Device not found"
- Pastikan Bluetooth aktif di kedua perangkat
- Pastikan perangkat dalam jangkauan (< 10 meter)
- Coba scan ulang perangkat

### Koneksi terputus
- Periksa jarak antar perangkat
- Pastikan tidak ada interferensi
- Restart Bluetooth jika perlu

## Keamanan

- Koneksi Bluetooth menggunakan enkripsi bawaan
- File transfer menggunakan encoding base64
- Tidak ada data yang disimpan di server eksternal
- Semua komunikasi bersifat peer-to-peer

## Limitasi

- Jangkauan terbatas pada range Bluetooth (biasanya ~10 meter)
- Kecepatan transfer file terbatas pada bandwidth Bluetooth
- Beberapa firewall atau antivirus mungkin memblokir koneksi Bluetooth
- Android 6+ memerlukan izin lokasi untuk scanning Bluetooth

## Kontribusi

Silakan buat issue atau pull request untuk perbaikan dan fitur baru.

## Lisensi

MIT License

## Tips

1. **Pairing**: Untuk koneksi yang lebih stabil, pair perangkat terlebih dahulu melalui pengaturan sistem
2. **Performance**: Transfer file kecil (<10MB) bekerja paling optimal
3. **Debugging**: Gunakan mode verbose dengan mengatur environment variable `DEBUG=1`
4. **Battery**: Koneksi Bluetooth yang aktif akan menggunakan baterai, terutama di mobile device

## FAQ

**Q: Apakah bisa digunakan tanpa internet?**
A: Ya, aplikasi ini sepenuhnya offline dan hanya menggunakan Bluetooth.

**Q: Berapa banyak perangkat yang bisa terhubung?**
A: Saat ini mendukung koneksi peer-to-peer (1-to-1).

**Q: Apakah file yang dikirim aman?**
A: Ya, menggunakan enkripsi Bluetooth standar dan tidak melewati server eksternal.

**Q: Kenapa scanning device lambat?**
A: Scanning Bluetooth membutuhkan waktu 8-10 detik untuk mendapatkan hasil yang lengkap.

**Q: Bisa kirim file berukuran besar?**
A: Secara teknis bisa, tapi disarankan file < 50MB untuk performa optimal.
