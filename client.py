import socket
import struct
import os
import threading
import sys
import time

HOST = "localhost"
PORT = 5000

os.makedirs("saved", exist_ok=True)
flag = False

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
    try:
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
    except socket.timeout:
        return "TIMEOUT"
    except Exception:
        return None

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

def listen(conn):
    while True:
        if flag:
            time.sleep(0.1)
            continue
        data = receive_msg(conn)

        if data == "TIMEOUT":
            continue

        if not data:
            print("\n[server disconnected]")
            os._exit(0) 
            
        print(f"\r\033[K[received messege]: {data}")
        print("input messege: ", end="", flush=True)


try: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c_sock:
        c_sock.connect((HOST, PORT))
        print(f"connected with: {HOST}")

        c_sock.settimeout(0.2)
        
        threads_listen = threading.Thread(target=listen, args=(c_sock,))
        threads_listen.daemon = True 
        threads_listen.start()
        
        while True:
            msg = input("input messege: ") 
            if not msg:
                continue

            if msg.startswith("/download "):
                flag = True
                time.sleep(0.3)
                c_sock.settimeout(None)
                send_msg(msg, c_sock)
                save_path = "saved/" + msg[10:]
                receive_file(c_sock, save_path)
                c_sock.settimeout(0.2)
                flag = False
                print(f"[downloaded file]: {msg[10:]}")
                continue
                
            elif msg.startswith("/upload "):
                flag = True
                time.sleep(0.3)
                c_sock.settimeout(None)
                send_msg(msg, c_sock)
                send_path = "saved/" + msg[8:]
                send_file(c_sock, send_path)
                c_sock.settimeout(0.2)
                flag = False
                print(f"[uploaded file]: {msg[8:]}")
                continue
            else:
                send_msg(msg, c_sock)

except Exception as e:
    print(f"\nconnection closed ({e})")