# color pixel picker
# HSV color model
# mask with cv
# tracking objects based on HSV color
#
import cv2 as cv

mainWin = "MyWin"
sideWin = "sideWin"
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
cv.namedWindow(mainWin)
cv.namedWindow(sideWin)

while True:
    _, frame = cap.read()

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frameHSV, (20,0,0), (40,255,255))
    frame2 = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow("MyWin", frame2)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()