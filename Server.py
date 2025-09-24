import socket
import sys
from smart_tv import SmartTV

tv = SmartTV()



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





#Communicate with the client
def handle_client(conn):
    try:
        while True:
            data=conn.recv(1024)
            if not data:
                break
            command = data.decode()
            result = handle_command(command)
            conn.sendall(result.encode())
    except Exception as e:
        print("Error during client communication:", e)

def main():
    host = '127.0.0.1'
    port= int(sys.argv[1]) if len(sys.argv) > 1 else 1238
    server_socket=create_socket()
    try: 
        bind_socket(server_socket,host,port)
        listen_for_connection(server_socket)
        conn,addr=accept_connection(server_socket)   #accepting one connection at a time
        print(f"Server connected with{addr}")
        conn.sendall(b"TV is off. only command allowed id turn_on\n")
        while True:
            command=receive_command(conn)   
            if not command or command.lower()=="turn_off":
                conn.sendall(b"The TV is turned off, Goodbye!\n")
                break
            response=handle_command(command)
            conn.sendall((response).encode())
    except:
        print("Server error")
    finally:
        close_socket(server_socket)

if __name__ =="__main__":
    main()

    