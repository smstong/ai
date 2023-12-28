# whac-a-mole
import numpy as np
import mediapipe as mp
import random
import math

# this module must be explicitly imported, as its parent module's __init__.py del it
# this is an "innternal" module which is not indended to be public API
from mediapipe.framework.formats import landmark_pb2

import cv2 as cv
import time
import winsound

g_screen_w = 800
g_screen_h = 600
R: mp.tasks.vision.HandLandmarkerResult = None

# sound api
# play a sound file asyncrously
def playsound_async(filename):
    winsound.PlaySound(
       filename, 
       winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOWAIT | winsound.SND_NOSTOP
       )

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
         
    
      # play sound
      if numRaised ==  2:
        playsound_async("Meow.wav")

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
    # whac the mole test
    if len(result.hand_landmarks) == 0: 
       return
    hand = result.hand_landmarks[0]
    tip = hand[8]
    point = (int(tip.x * g_screen_w), int(tip.y * g_screen_h))
    print(point)
    if math.sqrt((point[0]-g_mole["pos"][0])**2 + (point[1]-g_mole["pos"][1])**2) < g_mole["radius"]:
        move_mole()
        g_mole["score"] += 1
        #playsound_async("Meow.wav")
    print(g_mole)

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
cap.set(cv.CAP_PROP_FRAME_WIDTH, g_screen_w)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, g_screen_h)

g_mole = {
   "pos": (g_screen_w//2,g_screen_h//2),
   "radius": 100,
   "color": (0,0,244),
   "ms": 0,
   "score": 0,
}

def move_mole():
    x = random.randint(100,g_screen_w-100)
    y = random.randint(100,g_screen_h-100)
    g_mole["pos"] = (x,y)
    g_mole["ms"] = time.time_ns() / 1000000
   
def add_a_mole(frame):
    frameNew = np.copy(frame)
    ms = time.time_ns() / 1000000
    if ms - g_mole["ms"] > 1000:
        move_mole()

    font = cv.FONT_HERSHEY_COMPLEX
    fontScale = 10
    fontThick = 10
    text = f'{g_mole["score"]}'
    ((txt_w, txt_h),_) = cv.getTextSize(text, font, fontScale, fontThick)
    cv.circle(frameNew, g_mole["pos"], g_mole["radius"], (0,0,255), -1)
    cv.putText(frameNew, text, ((g_screen_w-txt_w)//2, (g_screen_h)//2), font, fontScale, (0,255,0), fontThick)
    return frameNew

while True:
    start_ms = time.time_ns()/1000000
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    detect_async(frame)
    frameRGB = draw_landmarks_on_image(frameRGB, R)
    #frameRGB = count_fingers_raised(frameRGB, R)

    frame = cv.cvtColor(frameRGB, cv.COLOR_RGB2BGR)
    frame = add_a_mole(frame)

    end_ms = time.time_ns()/1000000
    fps = 1000//(end_ms-start_ms)
    cv.putText(frame, f'fps:{fps}', (0,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)

    cv.imshow('Win', frame)
    if cv.waitKey(1) == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()
landmarker.close()
