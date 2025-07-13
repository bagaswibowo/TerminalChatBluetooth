#!/usr/bin/env python3
"""
RFCOMM Bluetooth Server untuk menerima chat dan file
Mendukung Linux dan Windows dengan PyBluez
"""

import bluetooth
import os
import time
import threading

class BluetoothServer:
    def __init__(self, port=1):
        self.port = port
        self.server_sock = None
        self.client_sock = None
        
    def start_server(self):
        """Mulai server RFCOMM Bluetooth"""
        try:
            # Buat socket RFCOMM
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            
            # Bind ke alamat local dan port
            self.server_sock.bind(("", self.port))
            
            # Listen untuk koneksi
            self.server_sock.listen(1)
            
            print(f"[SERVER] RFCOMM Server dimulai di port {self.port}")
            print("[SERVER] Menunggu koneksi client...")
            
            # Buat service advertised untuk discovery
            bluetooth.advertise_service(
                self.server_sock, 
                "TerminalChatBluetooth",
                service_id="1e0ca4ea-299d-4335-93eb-27fcfe7fa848",
                service_classes=[bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
            
            # Terima koneksi
            self.client_sock, client_info = self.server_sock.accept()
            print(f"[SERVER] Koneksi diterima dari {client_info}")
            
            # Handle komunikasi
            self.handle_client()
            
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
        finally:
            self.cleanup()
    
    def handle_client(self):
        """Handle komunikasi dengan client"""
        try:
            while True:
                # Terima data dari client
                data = self.client_sock.recv(1024)
                if not data:
                    print("[SERVER] Client disconnect")
                    break
                
                message = data.decode('utf-8').strip()
                print(f"[SERVER] Pesan diterima: {message}")
                
                if message.startswith("CHAT:"):
                    # Handle pesan chat
                    chat_msg = message[5:]  # Hilangkan prefix "CHAT:"
                    print(f"[CHAT] {chat_msg}")
                    
                    # Kirim ACK
                    self.client_sock.send("ACK: Pesan diterima".encode('utf-8'))
                    
                elif message.startswith("FILE:"):
                    # Handle transfer file
                    file_info = message[5:]  # Format: "FILE:nama_file:ukuran"
                    self.receive_file(file_info)
                    
                elif message == "QUIT":
                    print("[SERVER] Client request disconnect")
                    break
                    
        except Exception as e:
            print(f"[SERVER ERROR] Error handling client: {e}")
    
    def receive_file(self, file_info):
        """Terima file dari client"""
        try:
            # Parse info file: nama_file:ukuran
            parts = file_info.split(':')
            if len(parts) != 2:
                self.client_sock.send("ERROR: Format file info salah".encode('utf-8'))
                return
                
            filename = parts[0]
            file_size = int(parts[1])
            
            print(f"[SERVER] Menerima file: {filename} ({file_size} bytes)")
            
            # Kirim konfirmasi siap menerima
            self.client_sock.send("READY".encode('utf-8'))
            
            # Terima data file
            received_data = b""
            while len(received_data) < file_size:
                chunk = self.client_sock.recv(min(4096, file_size - len(received_data)))
                if not chunk:
                    break
                received_data += chunk
                
                # Progress indicator
                progress = (len(received_data) / file_size) * 100
                print(f"\r[SERVER] Progress: {progress:.1f}%", end='', flush=True)
            
            print()  # New line setelah progress
            
            # Simpan file dengan nama received_file.dat
            output_filename = "received_file.dat"
            with open(output_filename, 'wb') as f:
                f.write(received_data)
            
            print(f"[SERVER] File disimpan sebagai: {output_filename}")
            
            # Kirim konfirmasi
            self.client_sock.send("FILE_RECEIVED".encode('utf-8'))
            
        except Exception as e:
            print(f"[SERVER ERROR] Error receiving file: {e}")
            self.client_sock.send(f"ERROR: {str(e)}".encode('utf-8'))
    
    def cleanup(self):
        """Bersihkan resources"""
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()
        print("[SERVER] Server stopped")

def main():
    print("=== BLUETOOTH RFCOMM SERVER ===")
    print("Pastikan Bluetooth sudah enabled dan discoverable")
    print("Gunakan client.py untuk connect ke server ini")
    print()
    
    server = BluetoothServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Server dihentikan oleh user")
    except Exception as e:
        print(f"[SERVER ERROR] {e}")

if __name__ == "__main__":
    main()
