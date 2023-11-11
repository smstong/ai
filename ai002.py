#
# FPS cal
#
import cv2 as cv
import time

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
win = cv.namedWindow("MyWin")

start = 0
end = 0
while True:
    start = time.time()
    _, frame = cap.read()
    cv.imshow("MyWin", frame)

    end = time.time()
    spf = (end-start)
    fps = 1.0 / spf
    print(fps)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()