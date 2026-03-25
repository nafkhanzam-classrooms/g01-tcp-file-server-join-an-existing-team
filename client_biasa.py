import socket
import struct
import os

HOST = "localhost"
PORT = 5000

os.makedirs("saved", exist_ok=True)

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

def send_msg(data, conn):
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
try: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c_sock:
        c_sock.connect((HOST, PORT))

        print(f"connected with: {HOST}")
        
        while True:
            msg = input("input messege: ")
            if not msg:
                continue
            send_msg(msg, c_sock)

            if msg.startswith("/download "):
                save_path = "saved/" + msg[10:]
                receive_file(c_sock, save_path)
                print(f"[downloaded file]: {msg[10:]}")
                continue

            elif msg.startswith("/upload "):
                send_path = "saved/" + msg[8:]
                send_file(c_sock, send_path)
                print(f"[uploaded file]: {msg[8:]}")
                continue

            else:
                pass

            data = receive_msg(c_sock)
            if data:
                print(f"received messege: {data}\n")
            else:
                print("server closed")
                break
except:
    print("connection closed\n")