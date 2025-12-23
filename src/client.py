import socket
import datetime

CHUNK_SIZE = 1024

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def download_file(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        while True:
            filename = input("Enter filename to download (or type 'exit'): ")
            if filename.lower() == "exit":
                client_socket.sendall(b"exit")
                log("Exiting client session.")
                break

            client_socket.sendall(filename.encode())

            response = client_socket.recv(1024).decode()
            if response == "404 Not Found":
                log(f"File not found on server: {filename}")
                continue
            elif response != "200 OK":
                log(f"Unexpected server response: {response}")
                continue

            with open("downloaded_" + filename, "wb") as f:
                while True:
                    data = client_socket.recv(CHUNK_SIZE + 50)
                    if data == b"EOF":
                        log(f"File download completed: {filename}")
                        break

                    try:
                        header, chunk = data.split(b"|", 1)
                        seq_num = int(header.decode())
                        f.write(chunk)

                        ack_msg = f"ACK{seq_num}".encode()
                        client_socket.sendall(ack_msg)
                        log(f"Received chunk {seq_num}, sent {ack_msg.decode()}")
                    except Exception as e:
                        log(f"Error parsing chunk: {e}")

    except Exception as e:
        log(f"Connection error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8080
    download_file(server_host, server_port)
