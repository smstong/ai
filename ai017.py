# hand gesture
# (1) download model data
# (2) create gesture recognizer from options
# (3) call recognizer.recognize_async
# (4) anyalyse result in call back func
#
import numpy as np
import mediapipe as mp
import cv2 as cv
import time
import winsound

g_points = []
g_draw_mode = "none" # none, line, cicle, clear

# sound api
# play a sound file asyncrously
def playsound_async(filename):
    winsound.PlaySound(
       filename, 
       winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOWAIT | winsound.SND_NOSTOP
       )

# analyse result
def onResult(result: mp.tasks.vision.GestureRecognizerResult, img: mp.Image, timestamp_ms: int):
    global g_draw_mode
    curGesture = ""
    for gesture in result.gestures:
        print(gesture)
        curGesture = gesture[0].category_name
        break
    if curGesture == "Thumb_Down":
        g_draw_mode = "none"
    elif curGesture == "Thumb_Up":
        g_draw_mode = "line"
    elif curGesture == "Victory":
        pass
    elif curGesture == "Pointing_Up":
        pass
    elif curGesture == "Closed_Fist":
        pass
    elif curGesture == "Open_Palm":
        g_draw_mode = "clear"
    elif curGesture == "ILoveYou":
        pass
    else:
        pass
    
    if g_draw_mode == "clear":
        g_points.clear()
    if g_draw_mode == "line":
        # collect points
        for hand in result.hand_landmarks:
            index_tip = hand[8]
            x = int(index_tip.x*800)
            y = int(index_tip.y*600)
            # don't add duplicated points
            if len(g_points) > 0 and g_points[-1][0] == x and g_points[-1][1] == y:
                break

            g_points.append((x,y))

            # only count one hand
            break

# create gesture recoginizer object
options = mp.tasks.vision.GestureRecognizerOptions(
    base_options = mp.tasks.BaseOptions(model_asset_path='mediapipe/gesture_recognizer.task'),
    running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = 0.3,
    min_hand_presence_confidence = 0.3,
    min_tracking_confidence = 0.3,
    result_callback = onResult
    )
recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

# webcam init
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

# recognize a frame
def recognize_async(frame):
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    recognizer.recognize_async(image = mp_image, timestamp_ms = int(time.time()*1000))


# draw lines
def draw_lines(frame, color, thickness):
    # draw mode display
    cv.putText(frame, f"mode: {g_draw_mode}", (0,50), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0), 3)
    frameNew = np.copy(frame)
    for i in range(len(g_points)-1):
        cv.line(frameNew, g_points[i], g_points[i+1], color, thickness)
    return frameNew

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    if frame is None:
        print("error read")
        break

    recognize_async(frame)

    frame = draw_lines(frame, (0,0,255), 2)
    cv.imshow('Win', frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
recognizer.close()
