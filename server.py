import socket
import threading

# Jednoduchá databáze uživatelů
users = {
    "alice": "1234",
    "bob": "abcd",
    "charlie": "pass"
}

clients = {}

def broadcast(message, sender=None):
    for client in clients:
        try:
            client.send(f"{sender if sender else 'Server'}: {message}".encode())
        except:
            client.close()

def handle_client(client):
    try:
        client.send("USERNAME:".encode())
        username = client.recv(1024).decode().strip()

        client.send("PASSWORD:".encode())
        password = client.recv(1024).decode().strip()

        if users.get(username) != password:
            client.send("AUTH_FAILED".encode())
            client.close()
            return

        client.send("AUTH_SUCCESS".encode())
        broadcast(f"{username} has joined the chat!", "Server")
        clients[client] = username

        while True:
            msg = client.recv(1024).decode()
            if msg.lower() == "/quit":
                break
            broadcast(msg, sender=username)

    except:
        pass
    finally:
        client.close()
        if client in clients:
            broadcast(f"{clients[client]} has left the chat.", "Server")
            del clients[client]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 6000))
    server.listen(5)
    print("Chat server listening on port 6000...")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    main()
