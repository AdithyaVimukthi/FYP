# This code is for the server
# Lets import the libraries
import socket
import cv2
import pickle
import struct
import imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 8024
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Socket Accept
while True:
    conn, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if conn:
        vid = cv2.VideoCapture(0)

        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            conn.sendall(message)

            #cv2.imshow('TRANSMITTING VIDEO', frame)

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg}")
                else:
                    msg_part = msg.split()
                    print(msg_part[0], msg_part[1])

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
