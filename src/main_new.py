#!/usr/bin/env python3
import sys
import os
import platform

def main():
    print("=" * 60)
    print("    TERMINAL CHAT APPLICATION")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [mode] [connection_type]")
        print()
        print("Modes:")
        print("  server - Start as chat server")
        print("  client - Start as chat client")
        print()
        print("Connection Types:")
        print("  wifi   - Use WiFi/TCP connection (recommended)")
        print("  bt     - Use Bluetooth connection (experimental)")
        print()
        print("Examples:")
        print("  python main.py server wifi")
        print("  python main.py client wifi")
        print("  python main.py server bt")
        print("  python main.py client bt")
        print()
        print("Chat Commands:")
        print("  /send <filepath> - Send a file")
        print("  /quit - Exit the chat")
        return

    mode = sys.argv[1].lower()
    connection_type = sys.argv[2].lower() if len(sys.argv) > 2 else "wifi"

    if connection_type == "wifi":
        if mode == "server":
            from chat_server import ChatServer
            server = ChatServer()
            server.start_server()
            
        elif mode == "client":
            from chat_client import ChatClient
            client = ChatClient()
            
            print("Enter server details:")
            host = input("Server IP (default: localhost): ").strip() or "localhost"
            port_input = input("Server Port (default: 8888): ").strip()
            port = int(port_input) if port_input else 8888
            
            client.connect_to_server(host, port)
        else:
            print("Invalid mode. Use 'server' or 'client'.")
            
    elif connection_type == "bt":
        print(f"Platform detected: {platform.system()}")
        
        if mode == "server":
            try:
                from bluetooth_server import BluetoothChatServer
                import asyncio
                server = BluetoothChatServer()
                asyncio.run(server.start_server())
            except ImportError as e:
                print(f"Bluetooth not available: {e}")
                print("Please use 'wifi' mode instead.")
                
        elif mode == "client":
            try:
                from bluetooth_client import main as bt_client_main
                import asyncio
                asyncio.run(bt_client_main())
            except ImportError as e:
                print(f"Bluetooth not available: {e}")
                print("Please use 'wifi' mode instead.")
        else:
            print("Invalid mode. Use 'server' or 'client'.")
    else:
        print("Invalid connection type. Use 'wifi' or 'bt'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
