#!/usr/bin/env python3
"""
Bluetooth Chat Application - Client Mode
Aplikasi chat dan transfer file menggunakan koneksi Bluetooth
Author: Terminal Chat Bluetooth
"""

import bluetooth
import threading
import os
import json
import base64
from datetime import datetime
from colorama import init, Fore, Back, Style
import time

# Initialize colorama
init()

class BluetoothChatClient:
    def __init__(self):
        self.socket = None
        self.running = False
        
    def discover_devices(self):
        """Mencari perangkat Bluetooth yang tersedia"""
        print(f"{Fore.YELLOW}🔍 Mencari perangkat Bluetooth...{Style.RESET_ALL}")
        
        try:
            devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            
            if not devices:
                print(f"{Fore.RED}❌ Tidak ada perangkat Bluetooth ditemukan{Style.RESET_ALL}")
                return None
            
            print(f"{Fore.GREEN}📱 Perangkat ditemukan:{Style.RESET_ALL}")
            for i, (addr, name) in enumerate(devices):
                print(f"{Fore.CYAN}  {i+1}. {name} ({addr}){Style.RESET_ALL}")
            
            while True:
                try:
                    choice = input(f"\n{Fore.YELLOW}Pilih perangkat (1-{len(devices)}) atau 'q' untuk keluar: {Style.RESET_ALL}")
                    
                    if choice.lower() == 'q':
                        return None
                    
                    index = int(choice) - 1
                    if 0 <= index < len(devices):
                        return devices[index][0]  # Return MAC address
                    else:
                        print(f"{Fore.RED}❌ Pilihan tidak valid{Style.RESET_ALL}")
                        
                except ValueError:
                    print(f"{Fore.RED}❌ Masukkan angka yang valid{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Error mencari perangkat: {e}{Style.RESET_ALL}")
            return None
    
    def connect_to_server(self, server_addr, port=3):
        """Menghubungkan ke server Bluetooth"""
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print(f"{Fore.YELLOW}🔗 Menghubungkan ke {server_addr}...{Style.RESET_ALL}")
            
            self.socket.connect((server_addr, port))
            print(f"{Fore.GREEN}✅ Terhubung ke server!{Style.RESET_ALL}")
            
            self.running = True
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Start sending thread
            self.send_messages()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error menghubungkan ke server: {e}{Style.RESET_ALL}")
        finally:
            self.cleanup()
    
    def receive_messages(self):
        """Menerima pesan dari server"""
        while self.running:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                self.handle_message(message)
                
            except Exception as e:
                if self.running:
                    print(f"{Fore.RED}❌ Error menerima pesan: {e}{Style.RESET_ALL}")
                break
    
    def handle_message(self, message):
        """Menangani pesan yang diterima"""
        msg_type = message.get('type')
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if msg_type == 'text':
            print(f"{Fore.CYAN}[{timestamp}] Server: {message['content']}{Style.RESET_ALL}")
        
        elif msg_type == 'file':
            self.receive_file(message)
        
        elif msg_type == 'disconnect':
            print(f"{Fore.YELLOW}Server telah terputus{Style.RESET_ALL}")
            self.running = False
    
    def receive_file(self, message):
        """Menerima file dari server"""
        try:
            filename = message['filename']
            file_data = base64.b64decode(message['data'])
            
            # Create downloads directory if not exists
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            
            file_path = os.path.join(downloads_dir, filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{Fore.GREEN}[{timestamp}] 📁 File diterima: {filename} ({len(file_data)} bytes){Style.RESET_ALL}")
            print(f"{Fore.GREEN}   Disimpan di: {file_path}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error menerima file: {e}{Style.RESET_ALL}")
    
    def send_messages(self):
        """Mengirim pesan ke server"""
        print(f"{Fore.GREEN}✅ Terhubung! Ketik pesan atau gunakan perintah:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  /file <path> - Kirim file{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  /quit - Keluar{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Atau ketik pesan biasa untuk chat{Style.RESET_ALL}")
        print("-" * 50)
        
        while self.running:
            try:
                user_input = input()
                
                if user_input.lower() == '/quit':
                    self.send_disconnect()
                    break
                
                elif user_input.startswith('/file '):
                    file_path = user_input[6:].strip()
                    self.send_file(file_path)
                
                else:
                    self.send_text_message(user_input)
                    
            except KeyboardInterrupt:
                self.send_disconnect()
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error mengirim pesan: {e}{Style.RESET_ALL}")
    
    def send_text_message(self, text):
        """Mengirim pesan teks"""
        try:
            message = {
                'type': 'text',
                'content': text,
                'timestamp': datetime.now().isoformat()
            }
            
            data = json.dumps(message).encode('utf-8')
            self.socket.send(data)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{Fore.MAGENTA}[{timestamp}] Anda: {text}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error mengirim pesan: {e}{Style.RESET_ALL}")
    
    def send_file(self, file_path):
        """Mengirim file ke server"""
        try:
            if not os.path.exists(file_path):
                print(f"{Fore.RED}❌ File tidak ditemukan: {file_path}{Style.RESET_ALL}")
                return
            
            filename = os.path.basename(file_path)
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            file_b64 = base64.b64encode(file_data).decode('utf-8')
            
            message = {
                'type': 'file',
                'filename': filename,
                'data': file_b64,
                'timestamp': datetime.now().isoformat()
            }
            
            data = json.dumps(message).encode('utf-8')
            self.socket.send(data)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{Fore.GREEN}[{timestamp}] 📁 File terkirim: {filename} ({len(file_data)} bytes){Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error mengirim file: {e}{Style.RESET_ALL}")
    
    def send_disconnect(self):
        """Mengirim pesan disconnect"""
        try:
            message = {
                'type': 'disconnect',
                'timestamp': datetime.now().isoformat()
            }
            
            data = json.dumps(message).encode('utf-8')
            self.socket.send(data)
            
        except Exception as e:
            pass
        
        self.running = False
    
    def cleanup(self):
        """Membersihkan resource"""
        self.running = False
        
        if self.socket:
            self.socket.close()
        
        print(f"{Fore.YELLOW}🔴 Koneksi terputus{Style.RESET_ALL}")

def main():
    print(f"{Fore.BLUE}╔══════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║              BLUETOOTH CHAT CLIENT                   ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║            Chat & File Transfer via Bluetooth       ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    try:
        client = BluetoothChatClient()
        
        # Discover and select device
        server_addr = client.discover_devices()
        if server_addr:
            client.connect_to_server(server_addr)
        else:
            print(f"{Fore.YELLOW}Operasi dibatalkan{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🔴 Client dihentikan oleh user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
