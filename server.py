#!/usr/bin/env python3
"""
Bluetooth Chat Application - Server Mode
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

class BluetoothChatServer:
    def __init__(self, port=3):
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_info = None
        self.running = False
        
    def start_server(self):
        """Memulai server Bluetooth"""
        try:
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_socket.bind(("", self.port))
            self.server_socket.listen(1)
            
            print(f"{Fore.GREEN}🔵 Server Bluetooth dimulai pada port {self.port}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Menunggu koneksi client...{Style.RESET_ALL}")
            
            self.client_socket, self.client_info = self.server_socket.accept()
            print(f"{Fore.GREEN}✅ Client terhubung: {self.client_info}{Style.RESET_ALL}")
            
            self.running = True
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Start sending thread
            self.send_messages()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error memulai server: {e}{Style.RESET_ALL}")
        finally:
            self.cleanup()
    
    def receive_messages(self):
        """Menerima pesan dari client"""
        while self.running:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
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
            print(f"{Fore.CYAN}[{timestamp}] Client: {message['content']}{Style.RESET_ALL}")
        
        elif msg_type == 'file':
            self.receive_file(message)
        
        elif msg_type == 'disconnect':
            print(f"{Fore.YELLOW}Client telah terputus{Style.RESET_ALL}")
            self.running = False
    
    def receive_file(self, message):
        """Menerima file dari client"""
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
        """Mengirim pesan ke client"""
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
            self.client_socket.send(data)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{Fore.MAGENTA}[{timestamp}] Anda: {text}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error mengirim pesan: {e}{Style.RESET_ALL}")
    
    def send_file(self, file_path):
        """Mengirim file ke client"""
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
            self.client_socket.send(data)
            
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
            self.client_socket.send(data)
            
        except Exception as e:
            pass
        
        self.running = False
    
    def cleanup(self):
        """Membersihkan resource"""
        self.running = False
        
        if self.client_socket:
            self.client_socket.close()
        
        if self.server_socket:
            self.server_socket.close()
        
        print(f"{Fore.YELLOW}🔴 Server berhenti{Style.RESET_ALL}")

def main():
    print(f"{Fore.BLUE}╔══════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║              BLUETOOTH CHAT SERVER                   ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║            Chat & File Transfer via Bluetooth       ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    try:
        server = BluetoothChatServer()
        server.start_server()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🔴 Server dihentikan oleh user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
