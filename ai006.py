# tracking objects based on color
# yellow, blue
# red is special as it acrosses 180

import cv2 as cv
import numpy as np

mainWin = "MyWin"
sideWin = "sideWin"
barWin = "barWin"
minH = 0
maxH = 255
minS = 0
maxS = 255 
minV = 0
maxV = 255

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         color = frame[y, x]
         bgrImg = np.zeros((300,200,3), dtype=np.uint8) 
         bgrImg[:,:] = color
         b,g,r = color
         h,s,v = cv.cvtColor(bgrImg, cv.COLOR_BGR2HSV)[0,0]
         cv.putText(bgrImg, f"BGR:({b},{g},{r})", (50,100), cv.FONT_HERSHEY_PLAIN, 1, (255-int(b),255-int(g),255-int(r)), 2)
         cv.putText(bgrImg, f"HSV:({h},{s},{v})", (50,200), cv.FONT_HERSHEY_PLAIN, 1, (255-int(b),255-int(g),255-int(r)), 2)
         cv.imshow(sideWin, bgrImg)

def onMinH(v):
    global minH
    minH = v
def onMaxH(v):
    global maxH
    maxH = v
def onMinS(v):
    global minS
    minS = v
def onMaxS(v):
    global maxS
    maxS = v
def onMinV(v):
    global minV
    minV = v
def onMaxV(v):
    global maxV
    maxV = v

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
cv.namedWindow(mainWin)
cv.namedWindow(sideWin)
cv.setMouseCallback(mainWin, onMouse)
cv.namedWindow(barWin)
cv.createTrackbar("MinH", barWin, minH, 255, onMinH)
cv.createTrackbar("MaxH", barWin, maxH, 255, onMaxH)
cv.createTrackbar("MinS", barWin, minS, 255, onMinS)
cv.createTrackbar("MaxS", barWin, maxS, 255, onMaxS)
cv.createTrackbar("MinV", barWin, minV, 255, onMinV)
cv.createTrackbar("MaxV", barWin, maxV, 255, onMaxV)

while True:
    global frame
    _, frame = cap.read()

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frameHSV, (minH,minS,minV), (maxH,maxS,maxV))
    frame2 = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow("MyWin", frame2)
    cv.imshow("Mask", mask)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()