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
        print("🔍 Scanning for Bluetooth devices...")
        print("⏳ Please wait 10-15 seconds...")
        
        try:
            devices = await BleakScanner.discover(timeout=15.0)
            
            if not devices:
                print("❌ No Bluetooth devices found")
                print("💡 Troubleshooting checklist:")
                print("   1. Enable Bluetooth on both devices")
                print("   2. Make target device discoverable:")
                print("      • macOS: System Preferences > Bluetooth > Advanced")
                print("      • Windows: Settings > Devices > Bluetooth")
                print("      • Linux: bluetoothctl discoverable on")
                print("   3. Move devices closer (within 10 meters)")
                print("   4. Try running: python detect_bluetooth.py")
                return None
                
            print(f"\n✅ Found {len(devices)} devices:")
            print("━" * 60)
            
            valid_devices = []
            for i, device in enumerate(devices):
                device_name = device.name or "Unknown Device"
                device_addr = device.address
                
                # Get signal strength if available
                signal_info = ""
                if hasattr(device, 'rssi'):
                    signal_strength = device.rssi
                    if signal_strength > -50:
                        signal_info = " 📶 Strong"
                    elif signal_strength > -70:
                        signal_info = " 📶 Medium" 
                    else:
                        signal_info = " 📶 Weak"
                
                # Show device info clearly
                print(f"{len(valid_devices)+1:2d}. {device_name}")
                print(f"    🆔 Address: {device_addr}")
                print(f"    📡 Type: Bluetooth LE{signal_info}")
                
                # Try to identify if it's likely a computer
                if any(keyword in device_name.lower() for keyword in 
                      ['macbook', 'imac', 'pc', 'laptop', 'desktop', 'computer']):
                    print(f"    💻 Device Type: Computer (Good for chat)")
                elif any(keyword in device_name.lower() for keyword in 
                        ['phone', 'iphone', 'android', 'mobile']):
                    print(f"    📱 Device Type: Mobile")
                else:
                    print(f"    ❓ Device Type: Unknown")
                
                print("    " + "─" * 50)
                valid_devices.append(device)
                    
            if not valid_devices:
                print("❌ No valid devices found")
                return None
                
            print(f"\n💡 Tip: Look for devices marked as 'Computer' for chat servers")
            print(f"🔍 Need help? Run: python detect_bluetooth.py")
                
            return valid_devices
            
        except Exception as e:
            print(f"❌ Error scanning devices: {e}")
            
            # Specific error handling
            if "Bluetooth device is turned off" in str(e):
                print("💡 Solution: Enable Bluetooth on this device")
            elif "not authorized" in str(e).lower():
                print("💡 Solution: Grant Bluetooth permissions to this application")
            elif "no adapter" in str(e).lower():
                print("💡 Solution: Check if Bluetooth adapter is connected")
            else:
                print("💡 General solutions:")
                print("   • Check Bluetooth is enabled")
                print("   • Run as administrator/sudo if needed")
                print("   • Try: python detect_bluetooth.py --status")
                
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
