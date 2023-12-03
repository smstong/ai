# topic: hand detection and pose estimation with mediapipe
# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
import cv2 as cv
import numpy as np
import mediapipe as mp

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

hands = mp.solutions.hands.Hands(False, 2, min_detection_confidence=0.5,
                                 min_tracking_confidence = 0.5)
mpDraw = mp.solutions.drawing_utils

while True:
    _,frame = cap.read()
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks != None:
        for handMarks in results.multi_hand_landmarks:
            hand = []
            mpDraw.draw_landmarks(frame, handMarks,
                                  mp.solutions.hands.HAND_CONNECTIONS)
            for point in handMarks.landmark:
                hand.append((int(800*point.x), int(600*point.y)))
            cv.circle(frame, hand[20], 10, (255,0,0), -1)
    cv.imshow("Win", frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()