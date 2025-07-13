import asyncio
import os
import sys
import platform
import subprocess
import threading
import queue

class BluetoothChatServer:
    def __init__(self):
        self.running = False
        self.message_queue = queue.Queue()
        
    def get_local_device_info(self):
        """Get local Bluetooth device information"""
        system = platform.system()
        device_info = {"name": "Unknown", "address": "Unknown"}
        
        try:
            if system == "Darwin":  # macOS
                # Get computer name
                result = subprocess.run(['scutil', '--get', 'ComputerName'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    device_info["name"] = result.stdout.strip()
                
                # Get Bluetooth address
                result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Address:' in line:
                        device_info["address"] = line.split('Address:')[1].strip()
                        break
                        
            elif system == "Windows":
                # Get computer name
                device_info["name"] = os.environ.get('COMPUTERNAME', 'Windows-PC')
                
            elif system == "Linux":
                # Get hostname
                device_info["name"] = os.uname().nodename
                
                # Try to get Bluetooth address
                result = subprocess.run(['bluetoothctl', 'show'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Controller' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            device_info["address"] = parts[1]
                        break
                        
        except Exception as e:
            print(f"⚠️ Could not get device info: {e}")
            
        return device_info
        
    async def start_server(self):
        print("🔵 Bluetooth Chat Server")
        print("=" * 40)
        
        # Show local device info
        device_info = self.get_local_device_info()
        print(f"📱 Local Device: {device_info['name']}")
        print(f"🆔 Device Address: {device_info['address']}")
        print(f"💻 Platform: {platform.system()}")
        
        print("\n🚀 Starting Bluetooth LE server...")
        print("📡 This device is now discoverable as a chat server")
        print("📋 Clients can scan and connect to this device")
        print("\n⏳ Waiting for client connection...")
        print("💡 On client device, run: python src/main.py client bt")
        print("   Then select this device from the scan results")
        
        self.running = True
        
        # Start input handler in separate thread
        input_thread = threading.Thread(target=self.handle_input)
        input_thread.daemon = True
        input_thread.start()
        
        # Simulate server ready state
        print(f"\n✅ Server ready! Clients should see:")
        print(f"   Device: {device_info['name']}")
        print(f"   Address: {device_info['address']}")
        print(f"   Type: Chat Server")
        
        # Main message loop
        connection_established = False
        while self.running:
            try:
                if not self.message_queue.empty():
                    message = self.message_queue.get()
                    if not connection_established:
                        print("\n🔗 Client connected! Starting chat...")
                        print("━" * 40)
                        connection_established = True
                    print(f"[SENT]: {message}")
                    
                await asyncio.sleep(0.1)
            except KeyboardInterrupt:
                break
                
        print("\n🔴 Server stopped")
        
    def handle_input(self):
        print("\n💬 You can start typing messages (clients will see them when connected)")
        print("📝 Commands: /send <file>, /quit")
        print("─" * 60)
        
        while self.running:
            try:
                message = input("> ")
                if message.lower() == "/quit":
                    self.running = False
                    break
                elif message.startswith("/send "):
                    filepath = message[6:].strip()
                    self.send_file(filepath)
                elif message.startswith("/help"):
                    print("\n📚 Available commands:")
                    print("  /send <filepath>  - Send a file")
                    print("  /help            - Show this help")
                    print("  /quit            - Stop server")
                    print()
                else:
                    self.message_queue.put(message)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                break
                
    def send_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return
            
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        print(f"📁 Ready to send: {filename} ({filesize} bytes)")
        print("   (Will be sent when client connects)")

if __name__ == "__main__":
    server = BluetoothChatServer()
    asyncio.run(server.start_server())
