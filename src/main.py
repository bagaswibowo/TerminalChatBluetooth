import asyncio
import sys
from chat_server import ChatServer
from chat_client import ChatClient

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
        return

    mode = sys.argv[1]

    if mode == "server":
        server = ChatServer()
        await server.start()
    elif mode == "client":
        devices = ChatClient.discover_devices()
        if not devices:
            return
        
        for i, (addr, name) in enumerate(devices):
            print(f"{i}: {name} ({addr})")
        
        choice = input("Select a device to connect to: ")
        try:
            device_num = int(choice)
            if 0 <= device_num < len(devices):
                addr, name = devices[device_num]
                client = ChatClient(addr)
                await client.start()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Invalid mode. Use 'server' or 'client'.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
