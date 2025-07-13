#!/usr/bin/env python3
"""
RFCOMM Bluetooth Client untuk kirim chat dan file
Mendukung Linux dan Windows dengan PyBluez
"""

import bluetooth
import os
import time

class BluetoothClient:
    def __init__(self):
        self.sock = None
        self.connected = False
        
    def scan_devices(self):
        """Scan perangkat Bluetooth di sekitar"""
        print("[CLIENT] Scanning Bluetooth devices...")
        devices = bluetooth.discover_devices(duration=8, lookup_names=True)
        
        if not devices:
            print("[CLIENT] Tidak ada perangkat ditemukan")
            return None
            
        print("\n[CLIENT] Perangkat ditemukan:")
        for i, (addr, name) in enumerate(devices):
            print(f"{i+1}. {name} - {addr}")
        
        return devices
    
    def connect_to_server(self, server_addr, port=1):
        """Connect ke RFCOMM server"""
        try:
            print(f"[CLIENT] Connecting ke {server_addr}:{port}...")
            
            # Buat socket RFCOMM
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            
            # Connect ke server
            self.sock.connect((server_addr, port))
            self.connected = True
            
            print(f"[CLIENT] Berhasil connect ke {server_addr}")
            return True
            
        except Exception as e:
            print(f"[CLIENT ERROR] Gagal connect: {e}")
            return False
    
    def send_chat_message(self, message):
        """Kirim pesan chat"""
        if not self.connected:
            print("[CLIENT ERROR] Tidak terhubung ke server")
            return False
            
        try:
            # Format: CHAT:pesan
            formatted_msg = f"CHAT:{message}"
            self.sock.send(formatted_msg.encode('utf-8'))
            
            # Tunggu ACK dari server
            response = self.sock.recv(1024).decode('utf-8')
            print(f"[CLIENT] Server response: {response}")
            return True
            
        except Exception as e:
            print(f"[CLIENT ERROR] Error sending message: {e}")
            return False
    
    def send_file(self, file_path):
        """Kirim file ke server"""
        if not self.connected:
            print("[CLIENT ERROR] Tidak terhubung ke server")
            return False
            
        if not os.path.exists(file_path):
            print(f"[CLIENT ERROR] File tidak ditemukan: {file_path}")
            return False
            
        try:
            # Dapatkan info file
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            print(f"[CLIENT] Sending file: {filename} ({file_size} bytes)")
            
            # Kirim header file: FILE:nama_file:ukuran
            file_header = f"FILE:{filename}:{file_size}"
            self.sock.send(file_header.encode('utf-8'))
            
            # Tunggu konfirmasi server siap
            response = self.sock.recv(1024).decode('utf-8')
            if response != "READY":
                print(f"[CLIENT ERROR] Server tidak siap: {response}")
                return False
            
            # Kirim data file
            with open(file_path, 'rb') as f:
                sent_bytes = 0
                while sent_bytes < file_size:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    
                    self.sock.send(chunk)
                    sent_bytes += len(chunk)
                    
                    # Progress indicator
                    progress = (sent_bytes / file_size) * 100
                    print(f"\r[CLIENT] Progress: {progress:.1f}%", end='', flush=True)
            
            print()  # New line setelah progress
            
            # Tunggu konfirmasi dari server
            response = self.sock.recv(1024).decode('utf-8')
            if response == "FILE_RECEIVED":
                print("[CLIENT] File berhasil dikirim!")
                return True
            else:
                print(f"[CLIENT ERROR] Server error: {response}")
                return False
                
        except Exception as e:
            print(f"[CLIENT ERROR] Error sending file: {e}")
            return False
    
    def disconnect(self):
        """Disconnect dari server"""
        if self.connected:
            try:
                self.sock.send("QUIT".encode('utf-8'))
                self.sock.close()
                self.connected = False
                print("[CLIENT] Disconnected dari server")
            except:
                pass

def main():
    print("=== BLUETOOTH RFCOMM CLIENT ===")
    print()
    
    client = BluetoothClient()
    
    try:
        # Opsi 1: Scan dan pilih device
        print("1. Scan untuk mencari server")
        print("2. Connect langsung dengan alamat MAC")
        choice = input("Pilih opsi (1/2): ").strip()
        
        server_addr = None
        
        if choice == "1":
            devices = client.scan_devices()
            if devices:
                try:
                    selection = int(input("\nPilih nomor device untuk connect: ")) - 1
                    if 0 <= selection < len(devices):
                        server_addr = devices[selection][0]
                    else:
                        print("Pilihan tidak valid")
                        return
                except ValueError:
                    print("Input tidak valid")
                    return
        elif choice == "2":
            server_addr = input("Masukkan alamat MAC server: ").strip()
        else:
            print("Pilihan tidak valid")
            return
        
        if not server_addr:
            print("Alamat server tidak valid")
            return
        
        # Connect ke server
        if not client.connect_to_server(server_addr):
            return
        
        # Menu interaktif
        while True:
            print("\n=== MENU ===")
            print("1. Kirim pesan chat")
            print("2. Kirim file")
            print("3. Disconnect")
            
            choice = input("Pilih opsi (1-3): ").strip()
            
            if choice == "1":
                message = input("Masukkan pesan: ")
                if message:
                    client.send_chat_message(message)
                    
            elif choice == "2":
                file_path = input("Masukkan path file: ").strip()
                if file_path:
                    client.send_file(file_path)
                    
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid")
        
    except KeyboardInterrupt:
        print("\n[CLIENT] Client dihentikan oleh user")
    except Exception as e:
        print(f"[CLIENT ERROR] {e}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
