import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break

def write():
    while True:
        message = input()
        if message.lower() == "/exit":
            client.close()
            break

        full_message = f"{username}: {message}"
        try:
            client.send(full_message.encode("utf-8"))
        except:
            break

threading.Thread(target=receive).start()
threading.Thread(target=write).start()