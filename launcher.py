#!/usr/bin/env python3
"""
Terminal Chat Bluetooth - Smart Launcher
Automatically detects available libraries and launches appropriate version
"""

import sys
import subprocess

def check_bluetooth_support():
    """Check if PyBluez is available"""
    try:
        import bluetooth
        return True
    except ImportError:
        return False

def main():
    print("=== Terminal Chat Bluetooth Launcher ===")
    
    # Check for Bluetooth support
    has_bluetooth = check_bluetooth_support()
    
    if has_bluetooth:
        print("✅ Bluetooth support detected")
        print("🚀 Launching Bluetooth chat...")
        try:
            subprocess.run([sys.executable, "bluetooth_chat.py"], check=True)
        except FileNotFoundError:
            print("❌ bluetooth_chat.py not found")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running bluetooth chat: {e}")
            sys.exit(1)
    else:
        print("⚠️  PyBluez not available")
        print("🔄 Falling back to TCP chat for testing...")
        print("📝 To enable Bluetooth, install PyBluez:")
        print("   pip install pybluez")
        print("")
        
        try:
            subprocess.run([sys.executable, "tcp_chat_fallback.py"], check=True)
        except FileNotFoundError:
            print("❌ tcp_chat_fallback.py not found")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running TCP chat: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
