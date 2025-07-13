#!/usr/bin/env python3
"""
Termux-optimized version of Terminal Chat
Fallback to WiFi mode if Bluetooth is not available
"""

import sys
import os
import platform

def check_termux():
    """Check if running on Termux"""
    return os.path.exists('/data/data/com.termux')

def main():
    is_termux = check_termux()
    
    print("=" * 60)
    if is_termux:
        print("    TERMINAL CHAT - TERMUX ANDROID")
    else:
        print("    TERMINAL CHAT APPLICATION")
    print("=" * 60)
    print()
    
    if is_termux:
        print("🤖 Detected: Running on Termux Android")
        print("📡 Recommended: Use WiFi mode for best compatibility")
        print()
    
    if len(sys.argv) < 2:
        print("Usage: python termux_chat.py [mode] [connection_type]")
        print()
        print("Modes:")
        print("  server - Start as chat server")
        print("  client - Start as chat client")
        print()
        print("Connection Types:")
        print("  wifi   - Use WiFi/TCP connection (recommended for Termux)")
        print("  bt     - Use Bluetooth connection (experimental)")
        print()
        print("Examples:")
        print("  python termux_chat.py server wifi")
        print("  python termux_chat.py client wifi")
        if not is_termux:
            print("  python termux_chat.py server bt")
            print("  python termux_chat.py client bt")
        print()
        print("Chat Commands:")
        print("  /send <filepath> - Send a file")
        print("  /quit - Exit the chat")
        print()
        if is_termux:
            print("💡 Termux Tips:")
            print("  - Use 'ifconfig' to find your IP address")
            print("  - Use 'termux-setup-storage' for file access")
            print("  - Files save to: ~/received_<filename>")
        return

    mode = sys.argv[1].lower()
    connection_type = sys.argv[2].lower() if len(sys.argv) > 2 else "wifi"

    # Force WiFi mode on Termux if Bluetooth is requested but not available
    if is_termux and connection_type == "bt":
        try:
            import bleak
        except ImportError:
            print("⚠️  Bluetooth not available on this Termux installation")
            print("🔄 Falling back to WiFi mode...")
            connection_type = "wifi"

    if connection_type == "wifi":
        if mode == "server":
            from chat_server import ChatServer
            server = ChatServer()
            if is_termux:
                print("🤖 Termux: Server akan berjalan di semua interface")
                print("📱 Client lain bisa connect dengan IP Termux ini")
            server.start_server()
            
        elif mode == "client":
            from chat_client import ChatClient
            client = ChatClient()
            
            print("Enter server details:")
            if is_termux:
                print("💡 Tip: Gunakan IP address perangkat server (contoh: 192.168.1.100)")
            host = input("Server IP (default: localhost): ").strip() or "localhost"
            port_input = input("Server Port (default: 8888): ").strip()
            port = int(port_input) if port_input else 8888
            
            client.connect_to_server(host, port)
        else:
            print("Invalid mode. Use 'server' or 'client'.")
            
    elif connection_type == "bt":
        print(f"Platform detected: {platform.system()}")
        
        if is_termux:
            print("🤖 Termux Bluetooth mode detected")
            print("📱 Make sure:")
            print("   - Location Services ON")
            print("   - Bluetooth permission granted to Termux")
            print("   - Target device is discoverable")
            print()
        
        if mode == "server":
            try:
                from bluetooth_server import BluetoothChatServer
                import asyncio
                
                if is_termux:
                    print("⚠️  Note: Bluetooth server di Termux terbatas")
                    print("💡 Recommendation: Gunakan MacBook sebagai server")
                    print("🔄 Atau gunakan WiFi mode untuk reliability")
                    confirm = input("Continue with Bluetooth server? (y/N): ")
                    if confirm.lower() != 'y':
                        print("Switching to WiFi mode...")
                        from chat_server import ChatServer
                        server = ChatServer()
                        server.start_server()
                        return
                
                server = BluetoothChatServer()
                asyncio.run(server.start_server())
            except ImportError as e:
                print(f"❌ Bluetooth not available: {e}")
                print("💡 Install: pip install bleak")
                print("🔄 Or use WiFi mode: python termux_chat.py server wifi")
                
        elif mode == "client":
            try:
                from bluetooth_client import main as bt_client_main
                import asyncio
                
                if is_termux:
                    print("🔍 Scanning for Bluetooth devices...")
                    print("⏳ This may take 10-15 seconds...")
                    print("💡 Ensure target MacBook is discoverable")
                    print()
                
                asyncio.run(bt_client_main())
            except ImportError as e:
                print(f"❌ Bluetooth not available: {e}")
                print("💡 Install: pip install bleak")
                print("🔄 Or use WiFi mode: python termux_chat.py client wifi")
            except Exception as e:
                print(f"❌ Bluetooth error: {e}")
                print("💡 Common fixes:")
                print("   - Enable Location Services in Android")
                print("   - Grant Bluetooth permission to Termux")
                print("   - Make sure MacBook is discoverable")
                print("🔄 Try WiFi mode: python termux_chat.py client wifi")
        else:
            print("Invalid mode. Use 'server' or 'client'.")
    else:
        print("Invalid connection type. Use 'wifi' or 'bt'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
