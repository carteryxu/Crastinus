import cv2
import cv2.aruco
import numpy as np
import dlib
from math import hypot, sqrt
import pygame
import os
import time

font = cv2.FONT_HERSHEY_PLAIN
# Load the detector
detector = dlib.get_frontal_face_detector()
current_dir = os.path.dirname(os.path.abspath(__file__))
predictor_path = os.path.join(current_dir, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(predictor_path)

#Pygame + sound + image setup
pygame.init()
pygame.mixer.init()
unpleasant_sound = pygame.mixer.Sound(os.path.join(current_dir, "metal pipe falling sound effect.wav"))
unpleasant_image = cv2.imread(os.path.join(current_dir, "meekmillfocus.jpg"))

#Load camera
cap = cv2.VideoCapture(0)

# def midpoint(p1, p2):
#     return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

# def get_blinking_ratio(eye_points, facial_landmarks):
#     left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
#     right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
#     center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
#     center_bot = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

#     # Drawing horizontal and vertical line
#     # cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
#     # cv2.line(frame, center_top, center_bot, (0, 255, 0), 2)

#     # Calculating line ratios
#     vertical_length = hypot((center_top[0] - center_bot[0]), (center_top[1] - center_bot[1]))
#     horizontal_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    
#     ratio = horizontal_length / vertical_length
#     return ratio

def calibrate():
    calibration_points = [(100,00), (400, 100), (700, 100),
                          (100, 300), (400, 300), (700, 300),
                          (100, 500), (400, 500), (700, 500)]
    gaze_ratios = []

    for point in calibration_points:
        frame = np.zeros((600, 800, 3), np.uint8)
        cv2.circle(frame, point, 10, (0, 255, 0), -1)
        cv2.imshow('Calibration', frame)
        cv2.waitKey(1000)

        start_time = time.time()
        point_gaze_ratios = []
        while time.time() - start_time < 2.0:
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)
                gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
                gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
                gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2
                point_gaze_ratios.append(gaze_ratio)
        
        if point_gaze_ratios:
            gaze_ratios.append(np.mean(point_gaze_ratios))
    cv2.destroyWindow('Calibration')

    if len(gaze_ratios) == len(calibration_points):
        left_threshold = np.mean(gaze_ratios[0:3])
        center_threshold = np.mean(gaze_ratios[1:3])
        right_threshold = np.mean(gaze_ratios[2:3])
        up_threshold = np.mean(gaze_ratios[:3])
        down_threshold = np.mean(gaze_ratios[6:])

        return {
            'left': left_threshold,
            'center': center_threshold,
            'right': right_threshold,
            'up': up_threshold,
            'down': down_threshold
        }
    else:
        print("Calibration failed, reverting to default values.")
        return None


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
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    #Calculating the eye region (max and min x and y of landmark points)
    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])


    #Isolating just the eye region + thresholding the eye region (separating pupil and iris)
    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width/2)]
    right_eye_threshold = threshold_eye[0: height, int(width/2): width]
    #Counting size of whites
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_white = cv2.countNonZero(right_eye_threshold)

    #Preventing division by zero - crashing
    if right_side_white != 0:
        gaze_ratio = left_side_white / right_side_white
    else:
        gaze_ratio = 0

    return gaze_ratio

#Defining allowed gaze directions
allowed_gaze_direction = ["CENTER", "DOWN"]

def is_gaze_allowed(gaze_direction):
    return gaze_direction in allowed_gaze_direction

#Allowed time threshold
TIME_THRESHOLD = 1.0

start_time = None
SOUND_INTERVAL = 1.0

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
        # left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        # right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        # blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # if blinking_ratio > 4.45:
        #     cv2.putText(frame, "BLINKING", (50, 150), font, 10, (0, 0, 255), 5)

        #Gaze detection
        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2

        if gaze_ratio < 1:
            gaze_direction = "RIGHT"
        elif 1 <= gaze_ratio < 1.3:
            gaze_direction = "UP"
        elif 1.3 <= gaze_ratio < 1.565:
            gaze_direction = "CENTER"
        elif 1.7 <= gaze_ratio < 2.5:
            gaze_direction = "DOWN"
        else:
            gaze_direction = "LEFT"
        
        #cv2.putText(frame, "Gaze Ratio : " + str(gaze_ratio), (50, 100), font, 2, (0, 0, 255), 2)
        cv2.putText(frame, "Gaze Direction : " + gaze_direction, (50, 150), font, 4, (0, 255, 0), 3)

        #Gaze check
        if not is_gaze_allowed(gaze_direction):
            current_time = time.time()
            if start_time is None:
                start_time = current_time
            elif time.time() - start_time >= TIME_THRESHOLD:
                if current_time - start_time >= SOUND_INTERVAL:
                    pygame.mixer.Sound.play(unpleasant_sound)
                    start_time = current_time
                    cv2.imshow('Unpleasant Image', unpleasant_image)
        else:
            start_time = None
            pygame.mixer.Sound.stop(unpleasant_sound)
            cv2.destroyWindow('Unpleasant Image')


    #frame = cv2.flip(frame, 1)  ##Mirror the frame

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


