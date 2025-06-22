import socket
import threading
import sys
HOST = '127.0.0.1'
PORT = 5000
def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg, end="")
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        try:
            msg = input()
            if msg.strip().lower() == "/quit":
                break
            sock.sendall(msg.encode())
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    sock.close()

if __name__ == "__main__":
    main()
