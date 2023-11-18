# homework: control window movement based on color tracking

import cv2 as cv
import numpy as np

mainWin = "MyWin"

# by default, tracking "yellow"
minH = 24 
maxH = 36 
minS = 76 
maxS = 255 
minV = 158 
maxV = 255

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
cv.namedWindow(mainWin)

while True:
    global frame
    _, frame = cap.read()

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frameHSV, (minH,minS,minV), (maxH,maxS,maxV))

    # findContours works on mask
    # find external contours
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv.contourArea(contour) > 200:
            x,y,w,h = cv.boundingRect(contour)
            #cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            cv.moveWindow(mainWin, x, y)

    cv.imshow("MyWin", frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()