# Updated for new vesion mediapipe API
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv

# callback
def onResult(result, img, n):
    print(result)

# create an HanldLandmarker object
base_ptions = python.BaseOptions(model_asset_path='mediapipe/hand_landmarker.task')
# IMAGE mode
options = vision.HandLandmarkerOptions(base_options = base_ptions,
                                        running_mode = vision.RunningMode.IMAGE,
                                        num_hands = 1,
                                        )
detector = vision.HandLandmarker.create_from_options(options)
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

while True:
    _, frame = cap.read()
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    result = detector.detect(mp_image)

    # result is an object, which has 3 attributes 
    #print(type(result))

    # handedness is an arrary for each detected hand
    handedness = result.handedness
    for hand in handedness:
        # hand[0].index, 0 for right hand, 1 for left hand
        if hand[0].index == 0:
            print("Right hand")
        else:
            print("Left hand")

    # hand_landmarks is an array for each detected hand
    hand_landmarks = result.hand_landmarks
    # each landmark is an array of 21 kuckles (x,y,z)
    for landmark in hand_landmarks:
        # landmark[0] is the wrist
        x = int(800*landmark[8].x)
        y = int(600*landmark[8].y)
        print(x,y)
        cv.circle(frame, (x,y), 20, (0,0,255), 2)

    # hand_world_landmarks is an array for each detected hand
    hand_world_landmarks = result.hand_world_landmarks

    cv.imshow('Win', frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()

