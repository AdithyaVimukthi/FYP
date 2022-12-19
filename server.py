import socket
import threading

HEADER = 64
PORT = 5055
# SERVER = "192.168.11.240"
SERVER = "192.168.8.100"
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (socket family, socket type)
server.bind(ADDR)


def handle_client(conn, addr):
    global gripper
    print(f"[NEW CONNECTION] {addr} connected.")
    print("{:<20} {:<20} {:<20} {:<20}".format('Elbow angle', 'Shoulder angle', 'Gripper', 'Rotation'))
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

                if msg_part[2] == "1":
                    gripper = "gripped"
                if msg_part[2] == "0":
                    gripper = "grip off"

                print("{:<20} {:<20} {:<20} {:<20}".format(msg_part[0], msg_part[1], gripper, msg_part[3]))

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