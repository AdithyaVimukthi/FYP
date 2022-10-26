import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (socket family, socket type)
server.bind(ADDR)


def handle_client(conn, addr):
    global gripper
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] {msg}")
            else:
                msg_part = msg.split()

                if msg_part[2] == "0":
                    gripper = "gripped"
                if msg_part[2] == "1":
                    gripper = "grip off"

                print(f"[Elbow Angle] {msg_part[0]}  ///  [Shoulder Angle] {msg_part[1]} /// {gripper} /// [Rotation(%)] {msg_part[3]}")

            conn.send("Msg received".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting ........")
start()
