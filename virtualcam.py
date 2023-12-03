import pyvirtualcam as pvc
import numpy as np
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path='mediapipe/selfie_segmenter.tflite'),
    running_mode=VisionRunningMode.IMAGE,
    output_category_mask=True)

segmenter = vision.ImageSegmenter.create_from_options(options)

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv.CAP_PROP_FPS, 30)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv.CAP_PROP_FPS)

i = 0
with pvc.Camera(width, height, fps) as cam:
    print(f'Using virtual camera: {cam.device}')
    bgImage = cv.imread("flower-800x600.jpg")
    bgImage = cv.resize(bgImage, (width, height))
    while True:
        # read from physical cam
        _,frame = cap.read()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data=frame)
        segmentation_result = segmenter.segment(mp_image)
        category_mask = segmentation_result.category_mask
        
        condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1)
        output = np.where(condition, bgImage, frame)

        # convert to RGB and send to virtual cam
        cam.send(output)
        cam.sleep_until_next_frame()