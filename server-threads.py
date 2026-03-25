import socket
import threading
import os
import select
import struct
import json
import sys

HOST = "localhost"
PORT = 5000

os.makedirs("files", exist_ok=True)

client_list = []

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
    
    except Exception:
        return None

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

def multithr(conn, addr):
    print(f"connected with {addr}")
    client_list.append(conn)

    try:
        while True:
            data = receive_msg(conn)
            if data:
                print(f"from {addr}: {data}")

                if data == "/list":
                    list_files = os.listdir("files/.")
                    str_files = json.dumps(list_files)
                    send_msg(conn, str_files)

                elif data.startswith("/download "):
                    filename = "files/" + data[10:]
                    send_file(conn, filename)

                elif data.startswith("/upload "):
                    path = "files/" + data[8:]
                    receive_file(conn, path)
                    
                else:
                    broadcast = f"[{addr[1]}]: {data}"

                    for c_sock in list(client_list):
                        if c_sock != conn:
                            try:
                                send_msg(c_sock, broadcast)
                            except Exception:
                                pass
            else:
                break
                
    except Exception as e:
        print(f"error in client {addr}: {e}")
        
    finally:
        print(f"connection closed by {addr}")
        if conn in client_list:
            client_list.remove(conn)
        conn.close()


def broadcast_thread():
    while True:
        msg = sys.stdin.readline().strip()
        if msg:
            broadcast = f"[server]: {msg}"

            for client in list(client_list):
                try:
                    send_msg(client, broadcast)
                except Exception:
                    pass


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_s:
        serv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_s.bind((HOST, PORT))
        serv_s.listen(5)

        thread_server = threading.Thread(target=broadcast_thread)
        thread_server.daemon = True
        thread_server.start()

        while True:
            sock, addr = serv_s.accept()

            thread_client = threading.Thread(target=multithr, args=(sock, addr))
            thread_client.daemon =True
            thread_client.start()

except KeyboardInterrupt:
    print("\nserver closed.")
except Exception as e:
    print(f"\nserver error: {e}")