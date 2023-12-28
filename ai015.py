# Mediapipe runnming mode fro Live Stream.
# To do
# https://medium.com/@oetalmage16/a-tutorial-on-finger-counting-in-real-time-video-in-python-with-opencv-and-mediapipe-114a988df46a
import numpy as np
import mediapipe as mp

# this module must be explicitly imported, as its parent module's __init__.py del it
# this is an "innternal" module which is not indended to be public API
from mediapipe.framework.formats import landmark_pb2

import cv2 as cv
import time

R: mp.tasks.vision.HandLandmarkerResult = None

# draw number of raised fingures
def count_fingers_raised(rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
   try:
      # Get Data
      hand_landmarks_list = detection_result.hand_landmarks
      # Counter
      numRaised = 0
      # for each hand...
      for idx in range(len(hand_landmarks_list)):
         # hand landmarks is a list of landmarks where each entry in the list has an x, y, and z in normalized image coordinates
         hand_landmarks = hand_landmarks_list[idx]
         # for each fingertip... (hand_landmarks 4, 8, 12, and 16)
         for i in range(8,21,4):
            # make sure finger is higher in image the 3 proceeding values (2 finger segments and knuckle)
            tip_y = hand_landmarks[i].y
            dip_y = hand_landmarks[i-1].y
            pip_y = hand_landmarks[i-2].y
            mcp_y = hand_landmarks[i-3].y
            if tip_y < min(dip_y,pip_y,mcp_y):
               numRaised += 1
         # for the thumb
         # use direction vector from wrist to base of thumb to determine "raised"
         tip_x = hand_landmarks[4].x
         dip_x = hand_landmarks[3].x
         pip_x = hand_landmarks[2].x
         mcp_x = hand_landmarks[1].x
         palm_x = hand_landmarks[0].x
         if mcp_x > palm_x:
            if tip_x > max(dip_x,pip_x,mcp_x):
               numRaised += 1
         else:
            if tip_x < min(dip_x,pip_x,mcp_x):
               numRaised += 1
         
         
      # display number of fingers raised on the image
      annotated_image = np.copy(rgb_image)
      height, width, _ = annotated_image.shape
      text_x = int(hand_landmarks[0].x * width) - 100
      text_y = int(hand_landmarks[0].y * height) + 50
      cv.putText(img = annotated_image, text = str(numRaised) + " Fingers Raised",
                        org = (text_x, text_y), fontFace = cv.FONT_HERSHEY_DUPLEX,
                        fontScale = 1, color = (0,0,255), thickness = 2, lineType = cv.LINE_4)
      return annotated_image
   except:
      return rgb_image

# draw handmarks
def draw_landmarks_on_image(rgbImage, result:mp.tasks.vision.HandLandmarkerResult):
    if R is None:
        return rgbImage
    if len(R.hand_landmarks) == 0:
        return rgbImage
    annotated_image = np.copy(rgbImage)

    for hand in result.hand_landmarks:
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
            for landmark in hand])
        mp.solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style()
        )

    return annotated_image

# callback when result is ready
def onResult(result: mp.tasks.vision.HandLandmarkerResult, img: mp.Image, timestamp_ms: int):
    global R
    R = result

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options = mp.tasks.BaseOptions(model_asset_path='mediapipe/hand_landmarker.task'),
    running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM,
    num_hands = 2,
    min_hand_detection_confidence = 0.3,
    min_hand_presence_confidence = 0.3,
    min_tracking_confidence = 0.3,
    result_callback = onResult
    )
landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

def detect_async(frame):
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time()*1000))

# webcam init
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)

    detect_async(frame)

    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frameRGB = draw_landmarks_on_image(frameRGB, R)
    frameRGB = count_fingers_raised(frameRGB, R)

    frame = cv.cvtColor(frameRGB, cv.COLOR_RGB2BGR)
    cv.imshow('Win', frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
landmarker.close()
