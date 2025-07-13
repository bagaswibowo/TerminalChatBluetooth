#!/usr/bin/env python3
"""
Terminal Chat Bluetooth - Fallback Version
Simple TCP-based chat for testing when Bluetooth is not available
This version uses TCP sockets as a fallback when PyBluez is not available
"""

import os
import sys
import json
import base64
import socket
import threading
from pathlib import Path
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
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

class TCPChat:
    """Fallback TCP-based chat when Bluetooth is not available"""
    
    def __init__(self):
        self.socket = None
        self.client_socket = None
        self.is_server = False
        self.is_connected = False
        self.running = False
        self.username = os.getenv('USER', 'Unknown')
        self.chat_history = []
        self.port = 8888
        self.host = 'localhost'
        
        # File transfer settings
        self.chunk_size = 1024
        self.downloads_dir = Path.home() / "Downloads" / "TCPChat"
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"{Fore.CYAN}=== Terminal Chat TCP (Fallback Mode) ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}TCP-based chat for testing purposes{Style.RESET_ALL}")
        print(f"{Fore.RED}Note: This is fallback mode. For Bluetooth, install PyBluez.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Downloads will be saved to: {self.downloads_dir}{Style.RESET_ALL}")

    def print_colored(self, message, color=Fore.WHITE):
        """Print colored message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

    def start_server(self):
        """Start TCP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.is_server = True
            
            print(f"{Fore.GREEN}Server started on {self.host}:{self.port}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Waiting for client connection...{Style.RESET_ALL}")
            
            self.client_socket, client_address = self.socket.accept()
            print(f"{Fore.GREEN}Client connected: {client_address}{Style.RESET_ALL}")
            
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error starting server: {e}{Style.RESET_ALL}")
            return False

    def connect_to_server(self, host=None):
        """Connect to TCP server"""
        if host is None:
            host = input(f"{Fore.BLUE}Enter server IP (default: localhost): {Style.RESET_ALL}").strip()
            if not host:
                host = 'localhost'
        
        try:
            print(f"{Fore.YELLOW}Connecting to {host}:{self.port}...{Style.RESET_ALL}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, self.port))
            self.client_socket = self.socket
            self.is_connected = True
            
            print(f"{Fore.GREEN}Connected to {host}:{self.port}{Style.RESET_ALL}")
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
            
            json_data = json.dumps(data) + '\n'
            self.client_socket.send(json_data.encode('utf-8'))
            
            # Add to chat history
            self.chat_history.append(f"You: {message}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")
            return False

    def send_file(self, file_path):
        """Send a file"""
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
            
            self.client_socket.send((json.dumps(file_info) + '\n').encode('utf-8'))
            
            # Wait for confirmation
            response = self.client_socket.recv(1024).decode('utf-8').strip()
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
                            
                            encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                            chunk_data = {
                                'type': 'file_transfer',
                                'action': 'chunk',
                                'data': encoded_chunk
                            }
                            
                            self.client_socket.send((json.dumps(chunk_data) + '\n').encode('utf-8'))
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
                        
                        self.client_socket.send((json.dumps(chunk_data) + '\n').encode('utf-8'))
                        sent += len(chunk)
                        progress = (sent / file_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end='', flush=True)
                    print()
            
            # Send end signal
            end_signal = {
                'type': 'file_transfer',
                'action': 'end'
            }
            self.client_socket.send((json.dumps(end_signal) + '\n').encode('utf-8'))
            
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
        buffer = ""
        
        while self.running and self.is_connected:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line.strip():
                        continue
                    
                    try:
                        message_data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    if message_data['type'] == 'message':
                        username = message_data.get('username', 'Unknown')
                        content = message_data.get('content', '')
                        
                        self.print_colored(f"{username}: {content}", Fore.GREEN)
                        self.chat_history.append(f"{username}: {content}")
                    
                    elif message_data['type'] == 'file_transfer':
                        action = message_data.get('action')
                        
                        if action == 'file_info':
                            filename = message_data.get('filename')
                            file_size = message_data.get('size')
                            sender = message_data.get('username', 'Unknown')
                            
                            self.print_colored(f"File transfer request from {sender}: {filename} ({file_size} bytes)", Fore.YELLOW)
                            
                            # Auto-accept files
                            self.client_socket.send("ACCEPT\n".encode('utf-8'))
                            
                            # Prepare to receive file
                            current_file = self.downloads_dir / filename
                            file_handle = open(current_file, 'wb')
                            expected_size = file_size
                            received_size = 0
                            
                            self.print_colored(f"Accepting file: {filename}", Fore.GREEN)
                        
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
            for msg in self.chat_history[-10:]:
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
    chat = TCPChat()
    
    while True:
        print(f"\n{Fore.CYAN}=== TCP Chat Menu ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Start server{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Connect to server{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Exit{Style.RESET_ALL}")
        
        try:
            choice = input(f"{Fore.BLUE}Select option: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                if chat.start_server():
                    chat.start_chat()
            
            elif choice == '2':
                if chat.connect_to_server():
                    chat.start_chat()
            
            elif choice == '3':
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
