import socket
import os
import select
import struct
import json
import sys

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

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_s:
        serv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_s.bind((HOST, PORT))
        serv_s.listen(5)


        poll_object = select.poll()
        poll_object.register(serv_s, select.POLLIN)
        poll_object.register(sys.stdin, select.POLLIN)


        fd_map = {serv_s.fileno(): serv_s, sys.stdin.fileno(): sys.stdin}
        send_buf = {}

        while True:
            events = poll_object.poll()

            for fd, event in events:
                sock = fd_map[fd]

                if sock is serv_s:
                    client, addr = serv_s.accept()
                    fd_map[client.fileno()] = client
                    poll_object.register(client.fileno(), select.POLLIN)
                    print(f"connected with {addr}")

                elif sock == sys.stdin:
                    msg = sys.stdin.readline().strip()
                    if msg:
                        broadcast = f"[Server]: {msg}"

                        for client_fd, client_socket in fd_map.items():
                            if client_socket != serv_s and client_socket != sys.stdin:
                                try:
                                    send_msg(client_socket, broadcast)
                                except Exception:
                                    pass

                else:
                    data = receive_msg(sock)
                    
                    if data:
                        print(f"from {sock.getpeername()}: {data}")

                        if data == "/list":
                            list_files = os.listdir("files/.")
                            str_files = json.dumps(list_files)
                            send_msg(sock, str_files)

                        elif data.startswith("/download "):
                            filename = "files/" + data[10:]
                            send_file(sock, filename)

                        elif data.startswith("/upload "):
                            path = "files/" + data[8:]
                            receive_file(sock, path)
                            
                        else:
                            broadcast = f"[{sock.getpeername()[1]}]: {data}"
                            for client_fd, client_socket in fd_map.items():
                                if client_socket != serv_s and client_socket != sys.stdin and client_socket != sock:
                                    try:
                                        send_msg(client_socket, broadcast)
                                    except Exception:
                                        pass
                    else:
                        print(f"connection closed by {sock.getpeername()}")
                        poll_object.unregister(fd)
                        del fd_map[fd]
                        sock.close()

except KeyboardInterrupt:
    print("\nserver closed.")
except Exception as e:
    print(f"\nserver error: {e}")


