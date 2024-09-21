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
    # cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    # cv2.line(frame, center_top, center_bot, (0, 255, 0), 2)

    # Calculating line ratios
    vertical_length = hypot((center_top[0] - center_bot[0]), (center_top[1] - center_bot[1]))
    horizontal_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    
    ratio = horizontal_length / vertical_length
    return ratio

def get_gaze_ratio(eye_points, facial_landmarks):
    eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                        (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                        (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                        (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                        (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                        (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    #Creating mask
    height, width = frame.shape[:2]
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    #Calculating the eye region (max and min x and y of landmark points)
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])


    #Isolating just the eye region + thresholding the eye region (separating pupil and iris)
    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width/2)]
    right_eye_threshold = threshold_eye[0: height, int(width/2): width]
    #Counting size of whites
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_white = cv2.countNonZero(right_eye_threshold)

    gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


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
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio > 4.45:
            cv2.putText(frame, "BLINKING", (50, 150), font, 10, (0, 0, 255), 5)

        #Gaze detection
        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        

        cv2.putText(frame, "Gaze Ratio Left: " + str(gaze_ratio_left_eye), (50, 100), font, 2, (0, 0, 255), 2)
        cv2.putText(frame, "Gaze Ratio Right: " + str(gaze_ratio_right_eye), (50, 50), font, 2, (0, 0, 255), 2)


        
        



    #frame = cv2.flip(frame, 1)  ##Mirror the frame

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1000)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


