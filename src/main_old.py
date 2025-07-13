#!/usr/bin/env python3
import sys
import os

def main():
    print("=" * 50)
    print("    TERMINAL CHAT APPLICATION")
    print("=" * 50)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
        print()
        print("Commands:")
        print("  server - Start as chat server")
        print("  client - Start as chat client")
        print()
        print("Chat Commands:")
        print("  /send <filepath> - Send a file")
        print("  /quit - Exit the chat")
        return

    mode = sys.argv[1].lower()

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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
