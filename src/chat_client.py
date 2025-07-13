import asyncio
import bluetooth
from tui import TerminalTUI

class ChatClient:
    def __init__(self, host, port=4):
        self.host = host
        self.port = port

    async def start(self):
        print(f"Connecting to {self.host} on port {self.port}...")
        try:
            reader, writer = await asyncio.open_connection(
                self.host, self.port, family=bluetooth.AF_BLUETOOTH,
                proto=bluetooth.BTPROTO_RFCOMM
            )
            print("Connected!")
            tui = TerminalTUI(reader, writer)
            await tui.start()
        except (ConnectionRefusedError, OSError) as e:
            print(f"Connection failed: {e}")

    @staticmethod
    def discover_devices():
        print("Searching for devices...")
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print(f"Found {len(nearby_devices)} devices.")
        for addr, name in nearby_devices:
            print(f"  {addr} - {name}")
        return nearby_devices
