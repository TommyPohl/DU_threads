import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Zadej IP serveru: ")
    sock.connect((host, 6000))

    while True:
        prompt = sock.recv(1024).decode()
        if prompt == "USERNAME:":
            sock.send(input("Uživatelské jméno: ").encode())
        elif prompt == "PASSWORD:":
            sock.send(input("Heslo: ").encode())
        elif prompt == "AUTH_FAILED":
            print("Přihlášení selhalo. Zkontroluj údaje.")
            sock.close()
            return
        elif prompt == "AUTH_SUCCESS":
            print("Přihlášení úspěšné. Můžeš psát zprávy.")
            break

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "/quit":
            sock.send(msg.encode())
            break
        sock.send(msg.encode())

    sock.close()

if __name__ == "__main__":
    main()
