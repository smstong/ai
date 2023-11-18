# Homework: eyes detection
# eyes are always on a face

import cv2 as cv

mainWin = "MainWindow"

faceCascade = cv.CascadeClassifier("haardata/haarcascade_frontalface_default.xml")
eyeCascade = cv.CascadeClassifier("haardata/haarcascade_eye.xml")

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

cv.namedWindow(mainWin)

while True:
    _, frame = cap.read()

    # detect faces
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for face in faces:
       x, y, w, h = face 
       cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
       # detect eyes in face
       faceImg = gray[y:y+h, x:x+w]       
       eyes = eyeCascade.detectMultiScale(faceImg, 1.3, 5)
       for eye in eyes:
           xEye, yEye, wEye, hEye = eye
           cv.rectangle(frame, (x+xEye, y+yEye), (x+xEye+wEye, y+yEye+hEye), (0,0,255), 2)

    cv.imshow(mainWin, frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
