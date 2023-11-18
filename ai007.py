# change background (like Zoom's video effects)
# make object disappear

import cv2 as cv
import numpy as np

orgWin = "Origin"
mainWin = "MyWin"
sideWin = "sideWin"
barWin = "barWin"
minH = 0
maxH = 180
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
cv.namedWindow(orgWin)
cv.namedWindow(mainWin)
cv.namedWindow(sideWin)
cv.setMouseCallback(orgWin, onMouse)
cv.namedWindow(barWin)
cv.createTrackbar("MinH", barWin, minH, 180, onMinH)
cv.createTrackbar("MaxH", barWin, maxH, 180, onMaxH)
cv.createTrackbar("MinS", barWin, minS, 255, onMinS)
cv.createTrackbar("MaxS", barWin, maxS, 255, onMaxS)
cv.createTrackbar("MinV", barWin, minV, 255, onMinV)
cv.createTrackbar("MaxV", barWin, maxV, 255, onMaxV)

bg1 = cv.imread("flower-800x600.jpg")

while True:
    global frame
    _, frame = cap.read()

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frameHSV, (minH,minS,minV), (maxH,maxS,maxV))
    frame2 = cv.bitwise_and(frame, frame, mask=mask)

    maskRev = cv.bitwise_not(mask)
    bgFrame = cv.bitwise_and(bg1, bg1, maskRev)
    
    frame2 = cv.bitwise_or(frame2, bgFrame)

    cv.imshow(mainWin, frame2)
    cv.imshow(orgWin, frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()