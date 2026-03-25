import socket
import struct
import json
import os

HOST = "localhost"
PORT = 5000

os.makedirs("files", exist_ok=True)

def unique_name(path):
    if not os.path.exists(path):
        return path
    
    base_name, ext = os.path.splitext(path)
    num = 1

    while True:
        new_name = f"{base_name} ({num}){ext}"
        if not os.path.exists(new_name):
            return new_name
        num += 1

def receive_msg(conn):
    header = conn.recv(4)
    if not header:
            return None

    length = struct.unpack(">I", header)[0]
    buf = b""

    while len(buf) < length:
        chunk = conn.recv(length - len(buf))
        if not chunk:
            return None
        buf += chunk

    return buf.decode()

def receive_file(conn, path):
    path = unique_name(path)

    with open(path, "wb") as f:
        while True:
            header = conn.recv(4)
            if not header:
                break
            
            length = struct.unpack(">I", header)[0]
            if length == 0:
                break
            
            buf = b""
            while len(buf) < length:
                chunk = conn.recv(length - len(buf))
                if not chunk:
                    return None
                buf += chunk

            f.write(buf)


def send_msg(conn, data):
    data = data.encode()
    header = struct.pack(">I", len(data))
    conn.sendall(header + data)
    

def send_file(conn, path, chunk_size=4096):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            conn.sendall(struct.pack(">I", len(chunk)) + chunk)
    conn.sendall(struct.pack(">I", 0))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_serv:
        s_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_serv.bind((HOST, PORT))
        s_serv.listen(2)

        while True:
            sock, addr = s_serv.accept()
            with sock:
                print(f"connected with {addr}")

                while True:
                    data = receive_msg(sock)
                    if not data:
                        print(f"connected closed by: {addr}")
                        break

                    print(f"message from sender: {data}")

                    if data == "/list":
                        file_list = os.listdir("files/.")
                        list_str = json.dumps(file_list)
                        send_msg(sock, list_str)
                        continue

                    elif data.startswith("/download "):
                        filename = "files/" + data[10:]
                        send_file(sock, filename)
                        continue

                    elif data.startswith("/upload "):
                        path = "files/" + data[8:]
                        receive_file(sock, path)
                        continue
                        
                    else:
                        msg = input("write a message: ")
                        send_msg(sock, msg)
except KeyboardInterrupt:
    print("\nserver closed.")
except Exception as e:
    print(f"\nserver error: {e}")