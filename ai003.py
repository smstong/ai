#
# numpy ndarray demo
#
# - (B, G, R) color model in cv
# - ndarray range index
#
import cv2 as cv
import numpy as np

winName = "MyWin"
width = 800
height = 600

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
cv.namedWindow(winName)

def halfBlue(frame):
    frame[:,0:width//2] = (255,0,0)
    return frame

def reverseColor1(frame):
    for r in range(frame.shape[0]):
        for c in range(frame.shape[1]):
            oldColor = frame[r][c]
            frame[r][c] = (255-oldColor[0], 255-oldColor[1], 255-oldColor[2])
    return frame

def reverseColor2(frame):
    f = np.ones((600,800,3), dtype=np.uint8) 
    return 255*f - frame 

def reverseColor3(frame):
    return 255 - frame 

def defaultHandler(frame):
    return frame

handler = defaultHandler

while True:
    _, frame = cap.read()

    # processing frame here
    key = cv.waitKey(1)
    if key == ord('0'):
        handler = defaultHandler
    elif key == ord('1'):
        handler = halfBlue
    elif key == ord('2'):
        handler = reverseColor1
    elif key == ord('3'):
        handler = reverseColor2
    elif key == ord('4'):
        handler = reverseColor3
    else:
        pass

    frame = handler(frame)
    cv.imshow(winName, frame)

    if key == ord('q'):
        break

cap.release()