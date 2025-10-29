import socket
import sys
import threading

def create_client_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(sock, host, port):
    sock.connect((host, port))
    print("Connected to server")

def listen_for_updates(sock):
    """Lytter kontinuerlig etter meldinger fra serveren."""
    while True:
        try:
            message = sock.recv(4096).decode()
            if message:
                print("\n" + message + "\nIDATA2304>>", end="")
            else:
                break
        except:
            break

def read_send_command(sock):
    """Leser brukerinput og sender til serveren."""
    threading.Thread(target=listen_for_updates, args=(sock,), daemon=True).start()
    while True:
        command = input("IDATA2304>>")
        sock.sendall(command.encode())
        if command.lower() == "turn_off":
            break

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1238
    sock = create_client_socket()

    try:
        connect_to_server(sock, host, port)
        response = sock.recv(4096).decode(errors='ignore')
        print(response)
        read_send_command(sock)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
