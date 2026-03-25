import socket
import threading
import datetime

HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def log_message(message):
    with open("chat_log.txt", "a") as f:
        f.write(message + "\n")

def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message.encode("utf-8"))
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)
        client.close()

        leave_msg = f"{username} left the chat."
        print(leave_msg)
        log_message(leave_msg)
        broadcast(leave_msg)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                remove_client(client)
                break

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {message}"

            print(full_message)
            log_message(full_message)
            broadcast(full_message)

        except:
            remove_client(client)
            break

print(f"Server running on {HOST}:{PORT}")

while True:
    client, address = server.accept()
    print(f"Connected: {address}")

    client.send("USERNAME".encode("utf-8"))
    username = client.recv(1024).decode("utf-8")

    usernames.append(username)
    clients.append(client)

    join_msg = f"{username} joined the chat."
    print(join_msg)
    log_message(join_msg)
    broadcast(join_msg)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()