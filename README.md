# Terminal Chat Bluetooth

Aplikasi Python minimal untuk komunikasi chat dua arah dan transfer file antar laptop menggunakan Bluetooth RFCOMM dengan PyBluez.

## Fitur
- Chat dua arah melalui Bluetooth RFCOMM
- Transfer file antar perangkat
- Mendukung Linux dan Windows
- Interface terminal sederhana tanpa GUI

## Requirements
- Python 3.x
- PyBluez library
- Bluetooth adapter yang mendukung RFCOMM

## Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau manual:
```bash
pip install pybluez
```

### 2. Setup Bluetooth

#### Linux
```bash
# Jalankan script pairing
chmod +x pair_linux.sh
./pair_linux.sh

# Atau manual
sudo systemctl start bluetooth
sudo hciconfig hci0 up piscan
bluetoothctl
```

#### Windows
```cmd
REM Jalankan script pairing
pair_windows.bat

REM Atau manual via Settings > Devices > Bluetooth
```

## Penggunaan

### 1. Jalankan Server (Penerima)
Di laptop pertama:
```bash
python server.py
```

Output contoh:
```
=== BLUETOOTH RFCOMM SERVER ===
Pastikan Bluetooth sudah enabled dan discoverable

[SERVER] RFCOMM Server dimulai di port 1
[SERVER] Menunggu koneksi client...
[SERVER] Koneksi diterima dari ('XX:XX:XX:XX:XX:XX', 1)
```

### 2. Jalankan Client (Pengirim)
Di laptop kedua:
```bash
python client.py
```

Output contoh:
```
=== BLUETOOTH RFCOMM CLIENT ===

1. Scan untuk mencari server
2. Connect langsung dengan alamat MAC
Pilih opsi (1/2): 1

[CLIENT] Scanning Bluetooth devices...

[CLIENT] Perangkat ditemukan:
1. Laptop-Server - AA:BB:CC:DD:EE:FF
2. Phone-Device - 11:22:33:44:55:66

Pilih nomor device untuk connect: 1
[CLIENT] Connecting ke AA:BB:CC:DD:EE:FF:1...
[CLIENT] Berhasil connect ke AA:BB:CC:DD:EE:FF

=== MENU ===
1. Kirim pesan chat
2. Kirim file  
3. Disconnect
```

### 3. Test Chat
Pilih opsi 1 di client:
```
Pilih opsi (1-3): 1
Masukkan pesan: Halo dari client!
[CLIENT] Server response: ACK: Pesan diterima
```

Output di server:
```
[SERVER] Pesan diterima: CHAT:Halo dari client!
[CHAT] Halo dari client!
```

### 4. Test File Transfer
Pilih opsi 2 di client:
```
Pilih opsi (1-3): 2
Masukkan path file: example.txt
[CLIENT] Sending file: example.txt (156 bytes)
[CLIENT] Progress: 100.0%
[CLIENT] File berhasil dikirim!
```

Output di server:
```
[SERVER] Pesan diterima: FILE:example.txt:156
[SERVER] Menerima file: example.txt (156 bytes)
[SERVER] Progress: 100.0%
[SERVER] File disimpan sebagai: received_file.dat
```

## Struktur File
```
TerminalChatBluetooth/
├── server.py              # RFCOMM server
├── client.py              # RFCOMM client
├── example.txt             # Contoh file untuk transfer
├── requirements.txt        # Python dependencies
├── pair_linux.sh          # Script pairing Linux
├── pair_windows.bat       # Script pairing Windows
└── README.md              # Dokumentasi ini
```

## Troubleshooting

### Error: "Import bluetooth could not be resolved"
```bash
# Linux
sudo apt-get install python3-dev libbluetooth-dev
pip install pybluez

# Windows
pip install pybluez-win10
```

### Error: "No Bluetooth adapter found"
1. Pastikan Bluetooth adapter terpasang dan enabled
2. Restart Bluetooth service
3. Coba jalankan sebagai administrator/sudo

### Error: "Connection refused"
1. Pastikan kedua device sudah paired
2. Cek firewall tidak memblokir koneksi
3. Restart Bluetooth service di kedua device

### Error: "Device not found" 
1. Pastikan device dalam mode discoverable
2. Coba scan ulang dengan jarak lebih dekat
3. Hapus pairing lama dan pair ulang

## Catatan Teknis

### RFCOMM Protocol
- Menggunakan port 1 (default)
- Socket type: RFCOMM (reliable stream)
- Service UUID: Serial Port Profile

### Format Pesan
- Chat: `CHAT:isi_pesan`
- File: `FILE:nama_file:ukuran_bytes`
- Quit: `QUIT`

### File Transfer
- Chunk size: 4KB untuk optimasi
- File disimpan sebagai `received_file.dat`
- Progress indicator real-time

## Pengembangan Lebih Lanjut

Untuk mengembangkan aplikasi ini, Anda bisa menambahkan:
- Enkripsi untuk keamanan
- Multiple client connections
- GUI dengan tkinter/PyQt
- Kompresi file sebelum transfer
- Resume transfer yang terputus
- Chat history/logging
