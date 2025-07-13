import asyncio
import os
import sys
from bleak import BleakScanner, BleakClient
import threading
import queue

class BluetoothChatClient:
    def __init__(self):
        self.running = False
        self.message_queue = queue.Queue()
        
    async def discover_devices(self):
        print("Scanning for Bluetooth devices...")
        try:
            devices = await BleakScanner.discover(timeout=10.0)
            
            if not devices:
                print("No Bluetooth devices found")
                return None
                
            print(f"\nFound {len(devices)} devices:")
            for i, device in enumerate(devices):
                print(f"{i+1}. {device.name or 'Unknown'} ({device.address})")
                
            return devices
        except Exception as e:
            print(f"Error scanning devices: {e}")
            return None
            
    async def connect_to_device(self, device):
        try:
            print(f"Connecting to {device.name or 'Unknown'} ({device.address})...")
            
            async with BleakClient(device.address) as client:
                print(f"Connected to {device.name or 'Unknown'}!")
                
                self.running = True
                
                # Start input handler
                input_thread = threading.Thread(target=self.handle_input)
                input_thread.daemon = True
                input_thread.start()
                
                # Main communication loop
                while self.running:
                    try:
                        if not self.message_queue.empty():
                            message = self.message_queue.get()
                            print(f"[SENT]: {message}")
                        await asyncio.sleep(0.1)
                    except KeyboardInterrupt:
                        break
                        
        except Exception as e:
            print(f"Connection failed: {e}")
            
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

async def main():
    client = BluetoothChatClient()
    devices = await client.discover_devices()
    
    if devices:
        try:
            choice = int(input("\nSelect device number: ")) - 1
            if 0 <= choice < len(devices):
                await client.connect_to_device(devices[choice])
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    asyncio.run(main())
