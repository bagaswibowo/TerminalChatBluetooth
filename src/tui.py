import asyncio
import os

class TerminalTUI:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.running = False

    async def start(self):
        self.running = True
        asyncio.create_task(self.handle_input())
        await self.receive_messages()

    async def handle_input(self):
        while self.running:
            message = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            if message.lower() == "/quit":
                self.running = False
                self.writer.close()
                await self.writer.wait_closed()
                break
            elif message.lower().startswith("/send "):
                await self.send_file(message[6:].strip())
            else:
                self.writer.write(message.encode())
                await self.writer.drain()

    async def send_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        header = f"FILE:{file_name}:{file_size}\n"
        self.writer.write(header.encode())
        await self.writer.drain()

        with open(file_path, "rb") as f:
            self.writer.write(f.read())
            await self.writer.drain()
        print(f"File '{file_name}' sent.")

    async def receive_messages(self):
        while self.running:
            try:
                header_data = await self.reader.readuntil(b'\n')
                header = header_data.decode().strip()

                if header.startswith("FILE:"):
                    _, file_name, file_size_str = header.split(":", 2)
                    file_size = int(file_size_str)
                    
                    print(f"Receiving file: {file_name} ({file_size} bytes)")
                    
                    remaining_size = file_size
                    with open(file_name, "wb") as f:
                        while remaining_size > 0:
                            chunk = await self.reader.read(min(remaining_size, 4096))
                            if not chunk:
                                break
                            f.write(chunk)
                            remaining_size -= len(chunk)
                    print(f"File '{file_name}' received.")
                else:
                    print(f"\n< {header}")

            except asyncio.IncompleteReadError:
                print("Connection closed while receiving data.")
                break
            except asyncio.CancelledError:
                break
            except ConnectionResetError:
                print("Connection lost.")
                break
        self.running = False
