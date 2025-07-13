import asyncio
import bluetooth
from tui import TerminalTUI

class ChatServer:
    def __init__(self, port=4):
        self.port = port
        self.server_sock = None

    async def start(self):
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        print(f"Server listening on port {self.port}...")

        client_sock, client_info = await asyncio.get_event_loop().run_in_executor(
            None, self.server_sock.accept
        )
        print(f"Accepted connection from {client_info}")

        reader, writer = await asyncio.open_connection(sock=client_sock)
        tui = TerminalTUI(reader, writer)
        await tui.start()

    def stop(self):
        if self.server_sock:
            self.server_sock.close()
