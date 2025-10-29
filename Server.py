import socket
import sys
from smart_tv import SmartTV
import threading

tv = SmartTV()
clients = []           # list of all clients that are connected
lock = threading.Lock()  #protecting when multipli clients 



def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#associate socket with address of server
def bind_socket(sock,host,port):
    sock.bind((host,port))

def listen_for_connection(sock):
    sock.listen()
    #printing ip adress and portnumber of server
    print(f"Server listening on {sock.getsockname()}")  

def accept_connection(sock):
    conn,addr=sock.accept()
    print(f"Connected with {addr}")
    return conn,addr

def receive_command(conn):
    try:
        data=conn.recv(1024)
        if not data:
            return None
        return data.decode().strip()
    except:
        return "error during communication"

def close_socket(sock):
    sock.close()
    print("Server is closed")

def tv_menu():
    return(
        "Supported commands:\n"
            "- version\n"
            "- turn_on\n"
            "- turn_off\n"
            "- status\n"
            "- get_channel\n"
            "- get_channels\n"
            "- set_channel <number>\n"
            "- help\n"

    )
#For handeling commands in different versions
def handle_command(command: str):
    parts = command.strip().split(" ", 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if not tv.is_on and cmd != "turn_on":
        return "TV is off. Only command allowed is turn_on"

    if cmd == "version":
        return "TCP TV v1.0"
    elif cmd == "turn_on":
        tv.turn_on()
        return "TV turned ON\n" + tv.get_menu()
    elif cmd == "turn_off":
        tv.turn_off()
        return "TV turned OFF"
    elif cmd == "status":
        return tv.get_status()
    elif cmd == "get_channel":
        return f"Current channel: {tv.get_channel()}"
    elif cmd == "get_channels":
        return f"Total channels: {tv.get_channels()}"
    elif cmd == "set_channel":
        if not args.isdigit():
            return "Usage: set_channel <number>"
        number = int(args)
        if tv.set_channel(number):
            return f"Channel set to {number}"
        else:
            return f"Invalid channel. Allowed: 1-{tv.get_channels()}"
    elif cmd == "help":
        return tv.get_menu()
    else:
        return "Error: Unknown command"


#  Send message to all clients, adding broadcasting , lock makes it so multiple stings change clients at the same time, tunring on and off and so on
def broadcast(message, exclude_conn=None):
    with lock:
        for c in clients[:]:  # bruk kopi av lista i tilfelle noen kobles fra
            if c == exclude_conn:
                continue
            try:
                c.sendall(message.encode())
            except:
                clients.remove(c)



def handle_client(conn, addr):
    with lock:
        clients.append(conn)
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendall(b"TV is off. Only command allowed is turn_on\n")

    try:
        while True:
            command = receive_command(conn)
            if not command:
                break

            response = handle_command(command)
            conn.sendall(response.encode())

            # Hvis en klient endrer kanal, informer alle andre
            if command.lower().startswith("set_channel"):
                broadcast(f"[Notification] Channel changed to {tv.get_channel()} by {addr}\n", exclude_conn=conn)

            # Hvis noen skrur av TV-en
            if command.lower() == "turn_off":
                broadcast("[Notification] The TV has been turned OFF by someone.\n", exclude_conn=conn)
                break

    except Exception as e:
        print("Error during client communication:", e)
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")


# 
def main():
    host = '127.0.0.1'
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1238
    server_socket = create_socket()

    try:
        bind_socket(server_socket, host, port)
        listen_for_connection(server_socket)
        print("Waiting for clients...")

        while True:
            conn, addr = accept_connection(server_socket)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        close_socket(server_socket)


if __name__ == "__main__":
    main()