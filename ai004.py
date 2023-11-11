#
# drawings on frame
# mouse event
# gray out the selected region
# 
import cv2 as cv

rect = [0,0,0,0]

def onMouse(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        rect[0], rect[1] = x, y
        rect[2], rect[3] = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if flags == cv.EVENT_FLAG_LBUTTON:
            rect[2], rect[3] = x, y

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
win = cv.namedWindow("MyWin")
cv.setMouseCallback("MyWin", onMouse)

while True:
    _, frame = cap.read()

    cv.rectangle(frame, (100,100), (400,400), (255,0,0), 2)
    cv.circle(frame, (400,400), 100, (0,255,0), 2)
    cv.putText(frame, "Hello World", (100,100), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)

    # draw bounding rect of selected area
    cv.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,0), 2)

    # gray out the seleced region of the frame
    min1 = min(rect[0], rect[2])
    max1 = max(rect[0], rect[2])
    min2 = min(rect[1], rect[3])
    max2 = max(rect[1], rect[3])
    if min1 != max1 and min2 != max2:
        grayRect = cv.cvtColor(frame[min2:max2, min1:max1], cv.COLOR_BGR2GRAY)
        frame[min2:max2, min1:max1] = cv.cvtColor(grayRect, cv.COLOR_GRAY2BGR)

    cv.imshow("MyWin", frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()