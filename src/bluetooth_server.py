import asyncio
import os
import sys
from bleak import BleakScanner, BleakClient
from bleak.backends.service import BleakGATTService
from bleak.backends.characteristic import BleakGATTCharacteristic
import threading
import queue

class BluetoothChatServer:
    def __init__(self):
        self.running = False
        self.message_queue = queue.Queue()
        
    async def start_server(self):
        print("[SERVER] Starting Bluetooth LE server...")
        print("[SERVER] Advertising service for clients to connect...")
        
        # Untuk demo, kita akan simulasi server yang menunggu koneksi
        print("[SERVER] Bluetooth server ready!")
        print("[SERVER] Client dapat scan dan connect ke perangkat ini")
        print("[SERVER] Ketik pesan untuk mengirim:")
        
        self.running = True
        
        # Start input handler in separate thread
        input_thread = threading.Thread(target=self.handle_input)
        input_thread.daemon = True
        input_thread.start()
        
        # Main message loop
        while self.running:
            try:
                if not self.message_queue.empty():
                    message = self.message_queue.get()
                    print(f"[SENT]: {message}")
                await asyncio.sleep(0.1)
            except KeyboardInterrupt:
                break
                
        print("\n[SERVER] Stopped")
        
    def handle_input(self):
        while self.running:
            try:
                message = input("> ")
                if message.lower() == "/quit":
                    self.running = False
                    break
                elif message.startswith("/send "):
                    filepath = message[6:].strip()
                    self.send_file(filepath)
                else:
                    self.message_queue.put(message)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                break
                
    def send_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return
            
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        print(f"[FILE] Would send: {filename} ({filesize} bytes)")

if __name__ == "__main__":
    server = BluetoothChatServer()
    asyncio.run(server.start_server())
