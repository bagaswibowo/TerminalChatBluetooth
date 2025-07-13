#!/usr/bin/env python3
"""
Test script untuk koneksi Bluetooth Termux-MacBook
Usage: python test_bluetooth.py
"""

import asyncio
import os
import platform

def check_termux():
    return os.path.exists('/data/data/com.termux')

async def test_bluetooth_scan():
    """Test Bluetooth scanning capability"""
    print("🧪 Testing Bluetooth Scan Capability")
    print("=" * 40)
    
    is_termux = check_termux()
    if is_termux:
        print("🤖 Platform: Termux Android")
    else:
        print(f"💻 Platform: {platform.system()}")
    
    try:
        from bleak import BleakScanner
        print("✅ Bleak library available")
        
        print("\n🔍 Starting Bluetooth scan...")
        print("⏳ Scanning for 10 seconds...")
        
        devices = await BleakScanner.discover(timeout=10.0)
        
        if devices:
            print(f"\n✅ Found {len(devices)} devices:")
            for i, device in enumerate(devices):
                name = device.name or "Unknown"
                print(f"  {i+1}. {name}")
                print(f"     Address: {device.address}")
                if hasattr(device, 'rssi'):
                    print(f"     Signal: {device.rssi} dBm")
                print()
        else:
            print("\n❌ No devices found")
            
    except ImportError:
        print("❌ Bleak not installed")
        print("💡 Install with: pip install bleak")
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Troubleshooting tips
        print("\n🔧 Troubleshooting:")
        if is_termux:
            print("📱 For Termux Android:")
            print("   1. Enable Location Services in Android Settings")
            print("   2. Grant Bluetooth permission to Termux")
            print("   3. Make sure target MacBook is discoverable")
        else:
            print("💻 For macOS/Linux:")
            print("   1. Enable Bluetooth")
            print("   2. Make device discoverable")
            print("   3. Check privacy settings")

async def test_bluetooth_connection():
    """Test actual Bluetooth connection"""
    print("\n🔗 Testing Bluetooth Connection")
    print("=" * 40)
    
    try:
        from bleak import BleakScanner, BleakClient
        
        devices = await BleakScanner.discover(timeout=5.0)
        
        if not devices:
            print("❌ No devices found for connection test")
            return
            
        print("Available devices for test:")
        for i, device in enumerate(devices):
            print(f"  {i+1}. {device.name or 'Unknown'} ({device.address})")
            
        choice = input("\nSelect device for connection test (number, or Enter to skip): ")
        if not choice.strip():
            print("⏭️  Connection test skipped")
            return
            
        try:
            device_idx = int(choice) - 1
            if 0 <= device_idx < len(devices):
                test_device = devices[device_idx]
                print(f"\n🔄 Testing connection to {test_device.name or 'Unknown'}...")
                
                async with BleakClient(test_device.address) as client:
                    print(f"✅ Successfully connected to {test_device.name}!")
                    print(f"   Address: {test_device.address}")
                    print(f"   Connected: {client.is_connected}")
                    
            else:
                print("❌ Invalid device number")
                
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            
    except ImportError:
        print("❌ Bleak not available for connection test")

def print_setup_guide():
    """Print setup instructions"""
    print("\n📖 Setup Guide for Bluetooth Chat")
    print("=" * 40)
    
    is_termux = check_termux()
    
    if is_termux:
        print("🤖 Termux Android Setup:")
        print("1. pkg install python git")
        print("2. pip install bleak")
        print("3. Enable Location Services in Android")
        print("4. Grant Bluetooth permission to Termux")
        print("5. python termux_chat.py client bt")
        print()
        print("🍎 MacBook Setup (sebagai server):")
        print("1. Enable Bluetooth")
        print("2. Make MacBook discoverable")
        print("3. python src/main.py server bt")
    else:
        print("💻 Desktop Setup:")
        print("1. pip install bleak")
        print("2. Enable Bluetooth")
        print("3. python src/main.py server bt")
        print()
        print("📱 Termux Client:")
        print("1. python termux_chat.py client bt")

async def main():
    print("🔵 Bluetooth Test & Setup Tool")
    print("============================")
    
    await test_bluetooth_scan()
    await test_bluetooth_connection()
    print_setup_guide()
    
    print("\n✨ Test completed!")
    print("💡 If Bluetooth issues persist, use WiFi mode:")
    print("   python termux_chat.py server wifi")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted")
