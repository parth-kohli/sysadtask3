import socket
import threading
import hashlib
from datetime import datetime
from db import create_user, verify_user, log_message, start_session, end_session
from db import get_room_history, get_leaderboard
from db import create_room, get_all_rooms
HOST = '0.0.0.0'
PORT = 5000
clients = {}  
rooms = {}  

def broadcast(message, room, sender_sock=None):
    for client in rooms.get(room, []):
        if client != sender_sock:
            try:
                client.sendall(message.encode())
            except:
                pass

def handle_client(sock, addr):
    sock.send(b"Please /login <user> <pass> or /register <user> <pass>\n")
    username = None
    session_id = None
    while True:
        try:
            data = sock.recv(1024).decode().strip()
            if not data:
                break
            if data.startswith("/register"):
                parts = data.split()
                if len(parts) != 3:
                    sock.send(b"Usage: /register <username> <password>\n")
                    continue
                _, uname, pwd = parts
                try:
                    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
                    create_user(uname, pwd_hash)
                    sock.send(b"Registered. Please /login <user> <pass> now\n")
                except Exception as e:
                    sock.send(f"Registration failed: {e}\n".encode())
            elif data.startswith("/login"):
                parts = data.split()
                if len(parts) != 3:
                    sock.send(b"Usage: /login <username> <password>\n")
                    continue
                _, uname, pwd = parts
                pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
                if verify_user(uname, pwd_hash):
                    username = uname
                    session_id = start_session(uname)
                    clients[sock] = {"username": uname, "room": None}
                    sock.send(f"Welcome {uname}\n".encode())
                else:
                    sock.send(b"Login Failed\n")
                

            elif username:
                if data.startswith("/create"):
                    parts = data.split()
                    if len(parts) != 2:
                        sock.send(b"Usage: /create <room>\n")
                        continue
                    _, room = parts
                    if room in rooms:
                        sock.send(f"Room '{room}' exists\n".encode())
                    else:
                        create_room(room)
                        rooms[room] = set()
                        sock.send(f"Room '{room}' created\n".encode())

                elif data.startswith("/history"):
                    room = clients[sock]["room"]
                    if room:
                        history = get_room_history(room)
                        if history:
                            sock.send(b"\nLast messages:\n")
                            for sender, content, ts in history:
                                line = f"[{ts.strftime('%H:%M')}] {sender}: {content}\n"
                                sock.send(line.encode())
                        else:
                            sock.send(b"No message history\n")
                    else:
                        sock.send(b"You're not in a room\n")
                         
                elif data.startswith("/leaderboard"):
                    leaderboard = get_leaderboard()
                    if leaderboard:
                        sock.send(b"\nLeaderboard:\n")
                        for i, (sender, count) in enumerate(leaderboard, start=1):
                            line = f"{i}. {sender} - {count} messages\n"
                            sock.send(line.encode())
                    else:
                        sock.send(b"No messages yet\n")
                elif data.startswith("/join"):
                    parts = data.split()
                    if len(parts) != 2:
                        sock.send(b"Usage: /join <room>\n")
                        continue
                    _, room = parts
                    if room not in rooms:
                        sock.send(b"Room doesn't exist\n")
                    else:
                        if clients[sock]["room"]:
                            rooms[clients[sock]["room"]].discard(sock)
                        clients[sock]["room"] = room
                        rooms[room].add(sock)
                        sock.send(f"Joined room '{room}'\n".encode())
                        broadcast(f"{username} joined the room\n", room, sock)

                elif data.startswith("/leave"):
                    room = clients[sock]["room"]
                    if room:
                        rooms[room].discard(sock)
                        broadcast(f"{username} left the room\n", room, sock)
                        clients[sock]["room"] = None
                        sock.send(b"You left the room\n")
                    else:
                        sock.send(b"You are not in a room\n")

                elif data.startswith("/list"):
                    room_list = ", ".join(rooms.keys()) or "No active rooms"
                    sock.send(f"Rooms: {room_list}\n".encode())

                elif data.startswith("/whoami"):
                    sock.send(f"You are {username}\n".encode())

                elif data.startswith("/active"):
                    room = clients[sock]["room"]
                    if room:
                        users_in_room = [clients[c]["username"] for c in rooms[room]]
                        sock.send(f"Users in '{room}': {', '.join(users_in_room)}\n".encode())
                    else:
                        sock.send(b"You're not in a room\n")

                else:
                    room = clients[sock]["room"]
                    if room:
                        msg = f"{username}: {data}\n"
                        log_message(username, room, data)
                        broadcast(msg, room, sock)
                    else:
                        sock.send(b"Join a room to chat\n")
            else:
                sock.send(b" Please /login first\n")

        except Exception as e:
            print(f"[ERROR] {e}")
            break
    print(f"{addr} disconnected")
    if sock in clients:
        room = clients[sock]["room"]
        if room and sock in rooms.get(room, []):
            rooms[room].discard(sock)
            broadcast(f"{username} left\n", room, sock)
        del clients[sock]
    if session_id:
        end_session(session_id)
    sock.close()
def load_rooms():
    global rooms
    rooms = {}
    try:
        room_names = get_all_rooms()
        for room in room_names:
            rooms[room] = set()
        print(f"Loaded rooms: {list(rooms.keys())}")
    except Exception as e:
        print(f"Error loading rooms from DB: {e}")
def start_server():
    load_rooms()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Chat Server started on {HOST}:{PORT}")
    
    while True:
        client_sock, addr = server.accept()
        print(f"Connected: {addr}")
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

