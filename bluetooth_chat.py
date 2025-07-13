#!/usr/bin/env python3
"""
Terminal Chat Bluetooth - Main Application
Cross-platform Bluetooth chat with file transfer support
Compatible with macOS, Windows, Linux, and Termux
"""

import os
import sys
import time
import json
import base64
import socket
import threading
from pathlib import Path
from datetime import datetime

try:
    import bluetooth
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False
    print("Warning: PyBluez not installed. Install with: pip install pybluez")

try:
    from colorama import init, Fore, Back, Style
    init()  # Initialize colorama
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color codes
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    
    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

class BluetoothChat:
    def __init__(self):
        self.socket = None
        self.client_socket = None
        self.is_server = False
        self.is_connected = False
        self.running = False
        self.username = os.getenv('USER', 'Unknown')
        self.chat_history = []
        self.port = 1
        
        # File transfer settings
        self.chunk_size = 1024
        self.downloads_dir = Path.home() / "Downloads" / "BluetoothChat"
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"{Fore.CYAN}=== Terminal Chat Bluetooth ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Cross-platform offline chat with file transfer{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Downloads will be saved to: {self.downloads_dir}{Style.RESET_ALL}")

    def print_colored(self, message, color=Fore.WHITE):
        """Print colored message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

    def scan_devices(self):
        """Scan for nearby Bluetooth devices"""
        if not BLUETOOTH_AVAILABLE:
            print(f"{Fore.RED}Bluetooth not available. Please install PyBluez.{Style.RESET_ALL}")
            return []
        
        print(f"{Fore.YELLOW}Scanning for Bluetooth devices...{Style.RESET_ALL}")
        try:
            devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            print(f"\n{Fore.GREEN}Found {len(devices)} devices:{Style.RESET_ALL}")
            
            for i, (addr, name) in enumerate(devices, 1):
                print(f"{Fore.CYAN}{i}. {name} ({addr}){Style.RESET_ALL}")
            
            return devices
        except Exception as e:
            print(f"{Fore.RED}Error scanning devices: {e}{Style.RESET_ALL}")
            return []

    def start_server(self):
        """Start Bluetooth server"""
        if not BLUETOOTH_AVAILABLE:
            print(f"{Fore.RED}Bluetooth not available.{Style.RESET_ALL}")
            return False
        
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.bind(("", self.port))
            self.socket.listen(1)
            self.is_server = True
            
            print(f"{Fore.GREEN}Server started on port {self.port}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Waiting for client connection...{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Your device address: {bluetooth.read_local_bdaddr()[0]}{Style.RESET_ALL}")
            
            self.client_socket, client_info = self.socket.accept()
            print(f"{Fore.GREEN}Client connected: {client_info}{Style.RESET_ALL}")
            
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error starting server: {e}{Style.RESET_ALL}")
            return False

    def connect_to_device(self, address):
        """Connect to a Bluetooth device"""
        if not BLUETOOTH_AVAILABLE:
            print(f"{Fore.RED}Bluetooth not available.{Style.RESET_ALL}")
            return False
        
        try:
            print(f"{Fore.YELLOW}Connecting to {address}...{Style.RESET_ALL}")
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((address, self.port))
            self.client_socket = self.socket
            self.is_connected = True
            
            print(f"{Fore.GREEN}Connected to {address}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error connecting: {e}{Style.RESET_ALL}")
            return False

    def send_message(self, message):
        """Send a text message"""
        if not self.is_connected:
            print(f"{Fore.RED}Not connected to any device{Style.RESET_ALL}")
            return False
        
        try:
            data = {
                'type': 'message',
                'username': self.username,
                'content': message,
                'timestamp': datetime.now().isoformat()
            }
            
            json_data = json.dumps(data)
            self.client_socket.send(json_data.encode('utf-8'))
            
            # Add to chat history
            self.chat_history.append(f"You: {message}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")
            return False

    def send_file(self, file_path):
        """Send a file via Bluetooth"""
        if not self.is_connected:
            print(f"{Fore.RED}Not connected to any device{Style.RESET_ALL}")
            return False
        
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
            return False
        
        try:
            file_size = file_path.stat().st_size
            file_name = file_path.name
            
            # Send file info first
            file_info = {
                'type': 'file_transfer',
                'action': 'file_info',
                'filename': file_name,
                'size': file_size,
                'username': self.username
            }
            
            self.client_socket.send(json.dumps(file_info).encode('utf-8'))
            
            # Wait for confirmation
            response = self.client_socket.recv(1024).decode('utf-8')
            if response != "ACCEPT":
                print(f"{Fore.YELLOW}File transfer rejected{Style.RESET_ALL}")
                return False
            
            # Send file content
            print(f"{Fore.YELLOW}Sending file: {file_name} ({file_size} bytes){Style.RESET_ALL}")
            
            with open(file_path, 'rb') as f:
                if TQDM_AVAILABLE:
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as pbar:
                        while True:
                            chunk = f.read(self.chunk_size)
                            if not chunk:
                                break
                            
                            # Encode chunk as base64 and send
                            encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                            chunk_data = {
                                'type': 'file_transfer',
                                'action': 'chunk',
                                'data': encoded_chunk
                            }
                            
                            self.client_socket.send(json.dumps(chunk_data).encode('utf-8'))
                            pbar.update(len(chunk))
                else:
                    sent = 0
                    while True:
                        chunk = f.read(self.chunk_size)
                        if not chunk:
                            break
                        
                        encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                        chunk_data = {
                            'type': 'file_transfer',
                            'action': 'chunk',
                            'data': encoded_chunk
                        }
                        
                        self.client_socket.send(json.dumps(chunk_data).encode('utf-8'))
                        sent += len(chunk)
                        progress = (sent / file_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end='', flush=True)
                    print()  # New line after progress
            
            # Send end signal
            end_signal = {
                'type': 'file_transfer',
                'action': 'end'
            }
            self.client_socket.send(json.dumps(end_signal).encode('utf-8'))
            
            print(f"{Fore.GREEN}File sent successfully: {file_name}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error sending file: {e}{Style.RESET_ALL}")
            return False

    def receive_messages(self):
        """Receive messages in a separate thread"""
        current_file = None
        file_handle = None
        expected_size = 0
        received_size = 0
        
        while self.running and self.is_connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    message_data = json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    # Handle partial JSON data
                    continue
                
                if message_data['type'] == 'message':
                    username = message_data.get('username', 'Unknown')
                    content = message_data.get('content', '')
                    timestamp = message_data.get('timestamp', datetime.now().isoformat())
                    
                    self.print_colored(f"{username}: {content}", Fore.GREEN)
                    self.chat_history.append(f"{username}: {content}")
                
                elif message_data['type'] == 'file_transfer':
                    action = message_data.get('action')
                    
                    if action == 'file_info':
                        filename = message_data.get('filename')
                        file_size = message_data.get('size')
                        sender = message_data.get('username', 'Unknown')
                        
                        self.print_colored(f"File transfer request from {sender}: {filename} ({file_size} bytes)", Fore.YELLOW)
                        
                        # Auto-accept files (you can modify this to ask user)
                        accept = True
                        if accept:
                            self.client_socket.send("ACCEPT".encode('utf-8'))
                            
                            # Prepare to receive file
                            current_file = self.downloads_dir / filename
                            file_handle = open(current_file, 'wb')
                            expected_size = file_size
                            received_size = 0
                            
                            self.print_colored(f"Accepting file: {filename}", Fore.GREEN)
                        else:
                            self.client_socket.send("REJECT".encode('utf-8'))
                    
                    elif action == 'chunk' and file_handle:
                        chunk_data = base64.b64decode(message_data.get('data', ''))
                        file_handle.write(chunk_data)
                        received_size += len(chunk_data)
                        
                        if not TQDM_AVAILABLE:
                            progress = (received_size / expected_size) * 100
                            print(f"\rReceiving: {progress:.1f}%", end='', flush=True)
                    
                    elif action == 'end' and file_handle:
                        file_handle.close()
                        file_handle = None
                        print(f"\n{Fore.GREEN}File received: {current_file}{Style.RESET_ALL}")
                        current_file = None
                        received_size = 0
                        expected_size = 0
                
            except Exception as e:
                if self.running:
                    self.print_colored(f"Error receiving data: {e}", Fore.RED)
                break
        
        if file_handle:
            file_handle.close()

    def start_chat(self):
        """Start the chat session"""
        if not self.is_connected:
            print(f"{Fore.RED}Not connected to any device{Style.RESET_ALL}")
            return
        
        self.running = True
        
        # Start receiving thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        print(f"\n{Fore.GREEN}=== Chat Started ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}Commands:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/file <path> - Send a file{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/history - Show chat history{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/quit - Exit chat{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/help - Show this help{Style.RESET_ALL}\n")
        
        try:
            while self.running:
                message = input(f"{Fore.BLUE}> {Style.RESET_ALL}")
                
                if message.startswith('/'):
                    self.handle_command(message)
                else:
                    if message.strip():
                        self.send_message(message)
        
        except KeyboardInterrupt:
            self.print_colored("Chat interrupted by user", Fore.YELLOW)
        finally:
            self.disconnect()

    def handle_command(self, command):
        """Handle chat commands"""
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        
        if cmd == '/quit':
            self.running = False
            self.print_colored("Goodbye!", Fore.YELLOW)
        
        elif cmd == '/file':
            if len(parts) > 1:
                file_path = parts[1].strip()
                self.send_file(file_path)
            else:
                self.print_colored("Usage: /file <path>", Fore.YELLOW)
        
        elif cmd == '/history':
            self.print_colored("=== Chat History ===", Fore.CYAN)
            for msg in self.chat_history[-10:]:  # Show last 10 messages
                print(f"  {msg}")
        
        elif cmd == '/help':
            self.print_colored("Available commands:", Fore.CYAN)
            print(f"  {Fore.YELLOW}/file <path>{Style.RESET_ALL} - Send a file")
            print(f"  {Fore.YELLOW}/history{Style.RESET_ALL} - Show chat history")
            print(f"  {Fore.YELLOW}/quit{Style.RESET_ALL} - Exit chat")
            print(f"  {Fore.YELLOW}/help{Style.RESET_ALL} - Show this help")
        
        else:
            self.print_colored(f"Unknown command: {cmd}. Type /help for available commands.", Fore.RED)

    def disconnect(self):
        """Disconnect from current session"""
        self.running = False
        self.is_connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        
        if self.socket and self.is_server:
            try:
                self.socket.close()
            except:
                pass
        
        self.print_colored("Disconnected", Fore.YELLOW)

def main():
    """Main application entry point"""
    chat = BluetoothChat()
    
    while True:
        print(f"\n{Fore.CYAN}=== Main Menu ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Start server (wait for connection){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Connect to device{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Scan for devices{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Exit{Style.RESET_ALL}")
        
        try:
            choice = input(f"{Fore.BLUE}Select option: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                if chat.start_server():
                    chat.start_chat()
            
            elif choice == '2':
                devices = chat.scan_devices()
                if devices:
                    try:
                        device_num = int(input(f"{Fore.BLUE}Select device number (1-{len(devices)}): {Style.RESET_ALL}"))
                        if 1 <= device_num <= len(devices):
                            address = devices[device_num - 1][0]
                            if chat.connect_to_device(address):
                                chat.start_chat()
                        else:
                            print(f"{Fore.RED}Invalid device number{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
            
            elif choice == '3':
                chat.scan_devices()
            
            elif choice == '4':
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}Invalid option{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
