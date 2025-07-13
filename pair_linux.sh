#!/bin/bash
# Bluetooth Pairing Script untuk Linux

echo "=== BLUETOOTH PAIRING LINUX ==="
echo "Script untuk pairing perangkat Bluetooth di Linux"
echo

# Pastikan Bluetooth service berjalan
echo "1. Memastikan Bluetooth service aktif..."
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

echo "2. Mengaktifkan Bluetooth adapter..."
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan

echo "3. Scanning perangkat Bluetooth..."
echo "Scanning selama 10 detik..."
hcitool scan

echo
echo "4. Untuk pairing manual, gunakan bluetoothctl:"
echo "   sudo bluetoothctl"
echo "   scan on"
echo "   pair MAC_ADDRESS"
echo "   trust MAC_ADDRESS"
echo "   connect MAC_ADDRESS"
echo

echo "5. Atau gunakan script ini untuk pairing otomatis:"
echo -n "Masukkan MAC address perangkat target: "
read MAC_ADDR

if [ ! -z "$MAC_ADDR" ]; then
    echo "Melakukan pairing dengan $MAC_ADDR..."
    
    # Menggunakan bluetoothctl
    bluetoothctl << EOF
power on
agent on
default-agent
scan on
sleep 5
scan off
pair $MAC_ADDR
trust $MAC_ADDR
EOF

    echo "Pairing selesai. Coba jalankan server.py atau client.py"
else
    echo "MAC address tidak valid"
fi

echo
echo "=== TROUBLESHOOTING ==="
echo "Jika gagal:"
echo "1. Pastikan Bluetooth enabled: hciconfig"
echo "2. Restart Bluetooth: sudo systemctl restart bluetooth"
echo "3. Hapus pairing lama: bluetoothctl -> remove MAC_ADDRESS"
echo "4. Coba pairing ulang"
