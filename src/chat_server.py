import socket
import threading
import os
import sys

class ChatServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            print(f"[SERVER] Chat server started on {self.host}:{self.port}")
            print("[SERVER] Waiting for client connection...")
            print(f"[SERVER] Client dapat terhubung dengan: {self.host}:{self.port}")
            
            self.client_socket, address = self.server_socket.accept()
            print(f"[SERVER] Connected to {address}")
            
            self.running = True
            
            # Start receiver thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Handle user input
            self.handle_input()
            
        except Exception as e:
            print(f"Error starting server: {e}")
            
    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                    
                message = data.decode('utf-8')
                
                if message.startswith("FILE:"):
                    self.receive_file(message)
                else:
                    print(f"\n[CLIENT]: {message}")
                    print("> ", end="", flush=True)
                    
            except Exception as e:
                print(f"\nConnection error: {e}")
                break
                
        self.running = False
        
    def receive_file(self, header):
        try:
            parts = header.split(":")
            if len(parts) >= 3:
                filename = parts[1]
                filesize = int(parts[2])
                
                print(f"\n[FILE] Receiving: {filename} ({filesize} bytes)")
                
                with open(f"received_{filename}", "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = self.client_socket.recv(min(4096, filesize - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                        
                print(f"[FILE] Saved as: received_{filename}")
                print("> ", end="", flush=True)
                
        except Exception as e:
            print(f"Error receiving file: {e}")
            
    def send_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                return
                
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            
            # Send file header
            header = f"FILE:{filename}:{filesize}"
            self.client_socket.send(header.encode('utf-8'))
            
            # Send file content
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    self.client_socket.send(chunk)
                    
            print(f"[FILE] Sent: {filename}")
            
        except Exception as e:
            print(f"Error sending file: {e}")
            
    def handle_input(self):
        while self.running:
            try:
                message = input("> ")
                
                if message.lower() == "/quit":
                    break
                elif message.startswith("/send "):
                    filepath = message[6:].strip()
                    self.send_file(filepath)
                else:
                    self.client_socket.send(message.encode('utf-8'))
                    
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Error: {e}")
                break
                
        self.stop_server()
        
    def stop_server(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("\n[SERVER] Disconnected")

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
