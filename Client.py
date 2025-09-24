import socket
import sys


def create_client_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(sock, host, port):
    sock.connect((host,port))
    print("Connected to server")

def send_data(sock, message):
    sock.sendall(message.encode())

def recieve_data(sock, buffer_size = 4096):
    return sock.recv(buffer_size)

def read_send_command(sock):
    while True:
        command=input("IDATA2304>>")
        sock.sendall((command).encode())
        response=sock.recv(4096) .decode().strip()
        print(response)
        if command.lower()=="turn_off":
            break


def main():
    
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1238
    sock = create_client_socket()

    try:
        connect_to_server(sock, host, port)
        response = recieve_data(sock)
        print(response.decode(errors='ignore'))
        read_send_command(sock)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        sock.close()

#Steps for choosing own port and host
#first open a terminal in view and write python TvServer 5555  forexample
#Then open a new terminal and write python RemoteClient 127.0.0.1 5555  forexample


    
    

if __name__ == "__main__":
    main()

