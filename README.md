# Terminal Chat over Bluetooth

A simple terminal-based chat application that works over Bluetooth, allowing for offline communication and file transfer between various devices.

## Features

-   Cross-platform: Works on macOS, Windows, and Linux. Also supports Termux on Android.
-   Offline communication via Bluetooth.
-   Send and receive any type of file.
-   Simple terminal user interface.

## Prerequisites

-   Python 3.7+
-   Bluetooth adapter on your device.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd TerminalChatBluetooth
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The application has two modes: `server` and `client`. One device must act as the server, and the other as the client.

### Server Mode

To start the chat server, run the following command:

```bash
python src/main.py server
```

The server will start and wait for a client to connect.

### Client Mode

1.  To start the chat client, run the following command:
    ```bash
    python src/main.py client
    ```

2.  The client will scan for nearby Bluetooth devices and present a list.

3.  Select a device from the list by entering its number to establish a connection.

### Chatting

-   Simply type your message and press `Enter` to send.
-   Received messages will be displayed in the terminal.

### Sending Files

-   To send a file, use the `/send` command followed by the file path:
    ```
    > /send /path/to/your/file.jpg
    ```
-   You will see a confirmation once the file is sent. The receiver will see a message indicating that a file is being received.

### Quitting

-   To quit the chat, type `/quit` and press `Enter`.

## How It Works

The application uses the `PyBluez` library for Bluetooth communication. It sets up an RFCOMM socket for communication between the server and the client. The terminal user interface is built using Python's `asyncio` library to handle user input and network communication concurrently. File transfer is handled by sending a header with file information, followed by the file data in chunks.
