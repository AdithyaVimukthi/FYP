import mediapipe as mp
import cv2
import numpy as np
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.8.101"
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

def calculate_angle(a, b, c):
    a = np.array(a)  # Firstadi99
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(960,720))
        image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #color convert BGR to RGB
        results = holistic.process(image)           #make detection
        #print(results.pose_landmarks)              #print results top of the frame

        #mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2) #change colors of landmarks and landmark connections
        #mp_holistic.POSE_CONNECTIONS  mp_drawing.DrawingSpec(color=(240,0,0), thickness=2, circle_radius=2)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)#color convert RGB to BGR

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            hip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]
            shoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angle
            #angle = calculate_angle(shoulder, elbow, wrist)
            angle_elbow = round(calculate_angle(shoulder, elbow, wrist))
            angle_shoulder = round(calculate_angle(hip,shoulder, elbow))
            msg = str(angle_elbow) + "_" + str(angle_shoulder)
            send(msg)

            # Visualize angle
            cv2.putText(image, str(angle_elbow),
                        tuple(np.multiply(elbow, [960, 720]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2
                        )
            cv2.putText(image, str(angle_shoulder),
                        tuple(np.multiply(shoulder, [960, 720]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
                        )
        except:
            pass

        mp_drawing.draw_landmarks(image, results.right_hand_landmarks,mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 240, 0), thickness=2, circle_radius=1))   # Draw RIGHT hands landmarks
        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 240, 240), thickness=2, circle_radius=1))   #Draw pose landmarks
        #mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)             # Draw face landmarks
        #mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)        # Draw right hand landmarks
        #mp_drawing.plot_landmarks(results.pose_world_landmarks,mp_holistic.POSE_CONNECTIONS)

        cv2.imshow("Holistic Model", image)

        # Extract and draw pose on plain white image
        h, w, c = img.shape  # get shape of original frame
        opImg = np.zeros([h, w, c])  # create blank image with original frame size
        opImg.fill(0)  # set white background. put 0 if you want to make it black

        mp_drawing.draw_landmarks(opImg, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 240, 0), thickness=2,
                                                         circle_radius=1))  # Draw RIGHT hands landmarks
        mp_drawing.draw_landmarks(opImg, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 240, 240), thickness=2, circle_radius=1))

        cv2.imshow("skeleton", opImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            send(DISCONNECT_MESSAGE)
            break

cap.release()
cv2.destroyAllWindows()

print("Final angles:- ",angle_elbow,"////",angle_shoulder)
print("Thank You")