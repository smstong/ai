# color pixel picker
# HSV color model
# mask with cv
# tracking objects based on HSV color
#
import cv2 as cv
import numpy as np

mainWin = "MyWin"
sideWin = "sideWin"

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         color = frame[y, x]
         bgrImg = np.zeros((300,200,3), dtype=np.uint8) 
         bgrImg[:,:] = color
         b,g,r = color
         h,s,v = cv.cvtColor(bgrImg, cv.COLOR_BGR2HSV)[0,0]
         cv.putText(bgrImg, f"BGR:({b},{g},{r})", (50,100), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
         cv.putText(bgrImg, f"HSV:({h},{s},{v})", (50,200), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
         cv.imshow(sideWin, bgrImg)

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
cv.namedWindow(mainWin)
cv.namedWindow(sideWin)
cv.setMouseCallback(mainWin, onMouse)

while True:
    global frame
    _, frame = cap.read()

    #frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #mask = cv.inRange(frameHSV, (20,0,0), (40,255,255))
    #frame2 = cv.bitwise_and(frame, frame, mask=mask)

    frame2 = frame
    cv.imshow("MyWin", frame2)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()