# contours

import cv2 as cv
import numpy as np

mainWin = "MyWin"
sideWin = "sideWin"
barWin = "barWin"

# by default, tracking "yellow"
minH = 24 
maxH = 36 
minS = 76 
maxS = 255 
minV = 158 
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
cv.createTrackbar("MinH", barWin, minH, 180, onMinH)
cv.createTrackbar("MaxH", barWin, maxH, 180, onMaxH)
cv.createTrackbar("MinS", barWin, minS, 255, onMinS)
cv.createTrackbar("MaxS", barWin, maxS, 255, onMaxS)
cv.createTrackbar("MinV", barWin, minV, 255, onMinV)
cv.createTrackbar("MaxV", barWin, maxV, 255, onMaxV)

while True:
    global frame
    _, frame = cap.read()

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frameHSV, (minH,minS,minV), (maxH,maxS,maxV))

    # findContours works on mask
    # find external contours
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # draw ALL contours
    #cv.drawContours(frame2, contours, -1, (255,0,0), 2)

    for contour in contours:
        if cv.contourArea(contour) > 200:
            # draw contour
            #cv.drawContours(frame, [contour], 0, (255,0,0), 2)

            # draw bounding rect of contour
            x,y,w,h = cv.boundingRect(contour)
            cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)


    cv.imshow("MyWin", frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()