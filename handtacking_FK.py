import mediapipe as mp
import cv2
import numpy as np
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.8.100"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print(" ------Hello World------ ")
print("Wellcome to Hand Tracking")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(960,720))
        image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #color convert BGR to RGB
        results = holistic.process(image)           #make detection

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)#color convert RGB to BGR

        # Extract landmarks
        try:
            landmarks1 = results.pose_landmarks.landmark

        wrist1 = [landmarks1[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,
                  landmarks1[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]
        print( wrist1[0], "////", wrist1[1])


    except:
        pass


    if cv2.waitKey(1) & 0xFF == ord('q'):
        send(DISCONNECT_MESSAGE)
        break


cap.release()
cv2.destroyAllWindows()


print("Final end effector positions :- ",wrist1[0],"////",wrist1[1])
print("Thank You")