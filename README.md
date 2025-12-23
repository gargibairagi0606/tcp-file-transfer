# TCP File Transfer Application (Python)

A reliable TCP-based client-server application demonstrating **file transfer with chunking, acknowledgments, and retransmission**.  
Supports text, images, PDFs, and other file types. Implements **connection-oriented networking**, multi-file requests, and robust error handling.

## Key Concepts Demonstrated
- TCP connection-oriented file transfer
- Segmentation and chunking
- Acknowledgments and retransmission
- Threaded server for handling multiple clients concurrently
- Binary and text file support
- Clean, maintainable, and professional code structure
- Logging and timeout handling

## Project Structure

```
tcp-file-transfer/
├── src/
│ ├── client.py
│ └── server.py
├── README.md
└── .gitignore
```  
> Note: The server can transfer any file that exists on the server machine.
> Files may be located in the same directory as `server.py` or accessed using
> a relative or absolute file path when requested by the client.


## How to Run

### Start the Server

Open a terminal and run:

```bash
python src/server.py
```

The server will start listening for client connections.

### Start the Client

Open a new terminal and run:

```bash
python src/client.py
```

Type the filename to download:
```text
Enter filename to download (or type 'exit'): example.txt
```

- The client can request multiple files in a single session.
- Type `exit` to terminate the client.

### Example Output
**Client Side**
```
[2025-12-23 15:44:56] Received chunk 0, sent ACK0
[2025-12-23 15:44:56] Received chunk 1, sent ACK1
...
[2025-12-23 15:44:56] File download completed: example.txt
```


**Server Side**
```
[2025-12-23 15:44:56] Connected with ('127.0.0.1', 53693)
[2025-12-23 15:44:56] Client requested: example.txt
[2025-12-23 15:44:56] Sent chunk 0, waiting for ACK...
[2025-12-23 15:44:56] ACK received for chunk 0
...
[2025-12-23 15:44:56] File transfer completed: example.txt
```

### Notes

- The server supports multiple clients simultaneously using threading.
- Files of any type (.txt, .pdf, .jpg, .png, .docx, etc.) are supported.
- Binary mode is used to ensure file integrity across all formats.
- Timeouts apply only to ACK reception, triggering retransmission if needed.
- No example files are included to keep the repository clean and flexible.

### Skills Demonstrated

- Python socket programming
- TCP-based reliable file transfer
- Client–server system design
- Distributed systems fundamentals
- Error handling and timeout management
- Clean and maintainable code structure

### Optional Improvements

- Add a GUI-based client for easier file selection
- Support directory and batch downloads
- Add encryption for secure file transfer
- Log client activity to a file for monitoring
