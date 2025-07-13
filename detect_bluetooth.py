#!/usr/bin/env python3
"""
Bluetooth Device Detection and Helper
Untuk macOS, Windows, dan Linux
"""

import asyncio
import platform
import subprocess
import sys

async def detect_local_device():
    """Detect local Bluetooth device info"""
    system = platform.system()
    
    print(f"🔵 Platform: {system}")
    
    if system == "Darwin":  # macOS
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            output = result.stdout
            
            # Extract local device info
            for line in output.split('\n'):
                if 'Address:' in line and 'Local' in output:
                    address = line.split('Address:')[1].strip()
                    print(f"📱 Local Device Address: {address}")
                    break
                    
        except Exception as e:
            print(f"❌ Error getting macOS Bluetooth info: {e}")
            
    elif system == "Windows":
        try:
            # Try PowerShell command
            result = subprocess.run(['powershell', '-Command', 
                                   'Get-PnpDevice -Class Bluetooth | Where-Object {$_.Status -eq "OK"}'], 
                                  capture_output=True, text=True)
            if result.stdout:
                print("📱 Windows Bluetooth Devices:")
                print(result.stdout)
            else:
                print("💡 Check Bluetooth in Device Manager")
        except Exception as e:
            print(f"❌ Error getting Windows Bluetooth info: {e}")
            
    elif system == "Linux":
        try:
            # Check if bluetoothctl is available
            result = subprocess.run(['bluetoothctl', 'show'], 
                                  capture_output=True, text=True)
            if result.stdout:
                print("📱 Linux Bluetooth Info:")
                for line in result.stdout.split('\n'):
                    if 'Controller' in line or 'Name:' in line or 'Alias:' in line:
                        print(f"   {line.strip()}")
        except Exception as e:
            print(f"❌ Error getting Linux Bluetooth info: {e}")
            print("💡 Try: sudo apt install bluetooth bluez-utils")

async def scan_bluetooth_devices():
    """Scan for Bluetooth devices"""
    try:
        from bleak import BleakScanner
        
        print("\n🔍 Scanning for Bluetooth devices...")
        print("⏳ Please wait 10 seconds...")
        
        devices = await BleakScanner.discover(timeout=10.0)
        
        if devices:
            print(f"\n✅ Found {len(devices)} devices:")
            for i, device in enumerate(devices):
                device_name = device.name or "Unknown Device"
                rssi_info = f" (Signal: {device.rssi})" if hasattr(device, 'rssi') else ""
                print(f"   {i+1}. {device_name}")
                print(f"      Address: {device.address}{rssi_info}")
                print()
        else:
            print("\n❌ No Bluetooth devices found")
            print("💡 Make sure target devices are:")
            print("   - Bluetooth enabled")
            print("   - Set to discoverable")
            print("   - Within range (10 meters)")
            
    except ImportError:
        print("❌ Bleak library not installed")
        print("💡 Install with: pip install bleak")
    except Exception as e:
        print(f"❌ Scan error: {e}")
        if "turned off" in str(e).lower():
            print("💡 Enable Bluetooth on this device")
        elif "not authorized" in str(e).lower():
            print("💡 Grant Bluetooth permissions")

def check_bluetooth_status():
    """Check Bluetooth status on different platforms"""
    system = platform.system()
    
    print(f"\n🔧 Checking Bluetooth status on {system}...")
    
    if system == "Darwin":  # macOS
        try:
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True)
            if "State: On" in result.stdout:
                print("✅ Bluetooth is ON")
            else:
                print("❌ Bluetooth is OFF")
                print("💡 Enable: System Preferences > Bluetooth")
        except:
            print("❌ Cannot check Bluetooth status")
            
    elif system == "Windows":
        try:
            # Check Bluetooth service
            result = subprocess.run(['sc', 'query', 'bthserv'], 
                                  capture_output=True, text=True)
            if "RUNNING" in result.stdout:
                print("✅ Bluetooth service is running")
            else:
                print("❌ Bluetooth service not running")
                print("💡 Enable: Settings > Devices > Bluetooth")
        except:
            print("❌ Cannot check Bluetooth service")
            
    elif system == "Linux":
        try:
            result = subprocess.run(['systemctl', 'is-active', 'bluetooth'], 
                                  capture_output=True, text=True)
            if result.stdout.strip() == "active":
                print("✅ Bluetooth service is active")
            else:
                print("❌ Bluetooth service not active")
                print("💡 Start: sudo systemctl start bluetooth")
        except:
            print("❌ Cannot check Bluetooth service")

def show_connection_help():
    """Show connection help"""
    print("\n📖 Connection Help:")
    print("="*50)
    
    print("\n🎯 Step 1: Start Server")
    print("   python src/main.py server bt")
    print("   Note the device address shown")
    
    print("\n🎯 Step 2: Start Client")  
    print("   python src/main.py client bt")
    print("   Select server device from list")
    
    print("\n🔧 If connection fails:")
    print("   1. Make both devices discoverable")
    print("   2. Pair devices manually first")
    print("   3. Check firewall settings")
    print("   4. Try WiFi mode: python src/main.py server wifi")
    
    print("\n💡 Platform-specific tips:")
    
    system = platform.system()
    if system == "Darwin":
        print("   macOS: System Preferences > Bluetooth > Advanced")
        print("   ✅ Allow Bluetooth devices to find this Mac")
        
    elif system == "Windows":
        print("   Windows: Settings > Devices > Bluetooth")
        print("   ✅ Allow Bluetooth devices to find this PC")
        
    elif system == "Linux":
        print("   Linux: bluetoothctl discoverable on")
        print("   Run as sudo if needed")

async def test_bluetooth_connection():
    """Test basic Bluetooth functionality"""
    print("\n🧪 Testing Bluetooth Connection...")
    
    try:
        from bleak import BleakScanner, BleakClient
        
        # Quick scan
        devices = await BleakScanner.discover(timeout=5.0)
        
        if not devices:
            print("❌ No devices found for connection test")
            return
            
        print("📱 Available devices for test:")
        for i, device in enumerate(devices):
            print(f"   {i+1}. {device.name or 'Unknown'} ({device.address})")
            
        try:
            choice = input("\nSelect device number for connection test (or Enter to skip): ")
            if not choice.strip():
                print("⏭️ Connection test skipped")
                return
                
            device_idx = int(choice) - 1
            if 0 <= device_idx < len(devices):
                test_device = devices[device_idx]
                print(f"\n🔄 Testing connection to {test_device.name or 'Unknown'}...")
                
                async with BleakClient(test_device.address) as client:
                    print(f"✅ Connection successful!")
                    print(f"   Device: {test_device.name}")
                    print(f"   Address: {test_device.address}")
                    print(f"   Connected: {client.is_connected}")
                    
        except ValueError:
            print("❌ Invalid device number")
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            
    except ImportError:
        print("❌ Bleak not available for connection test")
        print("💡 Install: pip install bleak")

async def main():
    print("🔵 Bluetooth Detection & Helper Tool")
    print("="*40)
    
    # Detect local device
    await detect_local_device()
    
    # Check Bluetooth status
    check_bluetooth_status()
    
    # Scan for devices
    await scan_bluetooth_devices()
    
    # Test connection
    await test_bluetooth_connection()
    
    # Show help
    show_connection_help()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scan":
            asyncio.run(scan_bluetooth_devices())
        elif sys.argv[1] == "--info":
            asyncio.run(detect_local_device())
        elif sys.argv[1] == "--status":
            check_bluetooth_status()
        else:
            print("Usage: python detect_bluetooth.py [--scan|--info|--status]")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n⏹️ Detection interrupted")
