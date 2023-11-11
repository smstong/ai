#
# A simple hello world for opencv
#
import cv2 as cv

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
win = cv.namedWindow("MyWin")

while True:
    _, frame = cap.read()
    cv.imshow("MyWin", frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()