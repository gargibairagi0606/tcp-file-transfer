import socket
import threading
import os
import datetime

CHUNK_SIZE = 1024
ACK_TIMEOUT = 2

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def handle_client(conn, addr):
    log(f"Connected with {addr}")
    try:
        while True:
            filename = conn.recv(1024).decode()
            if not filename or filename.lower() == "exit":
                log(f"Client {addr} disconnected.")
                break

            log(f"Client requested: {filename}")

            if not os.path.exists(filename):
                conn.sendall(b"404 Not Found")
                log(f"File not found: {filename}")
                continue

            conn.sendall(b"200 OK")

            with open(filename, "rb") as f:
                seq_num = 0
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    packet = f"{seq_num}|".encode() + chunk
                    ack_received = False
                    while not ack_received:
                        conn.sendall(packet)
                        conn.settimeout(ACK_TIMEOUT)
                        try:
                            ack = conn.recv(1024).decode()
                            if ack == f"ACK{seq_num}":
                                log(f"ACK received for chunk {seq_num}")
                                ack_received = True
                                seq_num += 1
                            else:
                                log(f"Wrong ACK: {ack}, resending chunk {seq_num}")
                        except socket.timeout:
                            log(f"Timeout, resending chunk {seq_num}")

            conn.sendall(b"EOF")
            log(f"File transfer completed: {filename}")
            conn.settimeout(None)

    except Exception as e:
        log(f"Error: {e}")
    finally:
        conn.close()


def start_server(host="0.0.0.0", port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    log(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        log("Server shutting down gracefully.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
