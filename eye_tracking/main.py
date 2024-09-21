import cv2
import numpy as np
import dlib
from math import hypot, sqrt
import os

font = cv2.FONT_HERSHEY_PLAIN
# Load the detector
detector = dlib.get_frontal_face_detector()
current_dir = os.path.dirname(os.path.abspath(__file__))
predictor_path = os.path.join(current_dir, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(predictor_path)


#Load camera
cap = cv2.VideoCapture(0)

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bot = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # Drawing horizontal and vertical line
    cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    cv2.line(frame, center_top, center_bot, (0, 255, 0), 2)

    # Calculating line ratios
    vertical_length = hypot((center_top[0] - center_bot[0]), (center_top[1] - center_bot[1]))
    horizontal_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    
    ratio = horizontal_length / vertical_length
    return ratio


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        #Detect blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47, 48], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio > 4.45:
            cv2.putText(frame, "BLINKING", (50, 150), font, 10, (0, 0, 255), 5)

        #Gaze detection
        left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                    (landmarks.part(37).x, landmarks.part(37).y),
                                    (landmarks.part(38).x, landmarks.part(38).y),
                                    (landmarks.part(39).x, landmarks.part(39).y),
                                    (landmarks.part(40).x, landmarks.part(40).y),
                                    (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
        cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)
        



    #frame = cv2.flip(frame, 1)  ##Mirror the frame

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


