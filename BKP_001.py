import mediapipe as mp
import cv2

print(" ------Hello World------ ")
print("Wellcome to Hand Tracking")

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        success, img = cap.read()

        image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #color convert BGR to RGB
        results = holistic.process(image)           #make detection
        #print(results.pose_landmarks)              #print results top of the frame

        #mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2) #change colors of landmarks and landmark connections
        #mp_holistic.POSE_CONNECTIONS  mp_drawing.DrawingSpec(color=(240,0,0), thickness=2, circle_radius=2)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)#color convert RGB to BGR

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            #print(landmarks)
        except:
            pass

        print("LEFT_SHOULDER")
        print(landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value])
        print("LEFT_ELBOW")
        print(landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value])
        print("LEFT_WRIST")
        print(landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value])

        #print(len(landmarks))

        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(240, 0, 0), thickness=2, circle_radius=2)
                                  )                                                                     #Draw pose landmarks
        #mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)        # Draw face landmarks
        #mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)   # Draw right hand landmarks
        #mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)    # Draw left hands landmarks

        cv2.imshow("Holistic Model", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

print("Thank You")