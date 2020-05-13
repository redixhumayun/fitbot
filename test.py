import time
import cv2
import sys
import numpy as np
from picameravideostream import PiCameraVideoStream

# Setting this to output full numpy array and not truncated form
np.set_printoptions(threshold=sys.maxsize)

# Set of classes that OpenCV is set up to detect as an object
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# Generate a random color in each class
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Load the caffe model and prototxt file
net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt.txt", "model/MobileNetSSD_deploy.caffemodel")

# Start the video stream and sleep for 2s to warm up camera sensor
video_stream = PiCameraVideoStream().start()
time.sleep(2.0)

start = time.time()


while True:
  frame = video_stream.read()

  # This frame has the shape (240, 320, 3) which implies that there are 240 rows
  # each row has a width of 320 and the inner most value is the RGB value of a 
  # particular pixel
  (h, w) = frame.shape[:2]
  resized_frame = cv2.resize(frame, (300, 300))
  blob = cv2.dnn.blobFromImage(resized_frame, 0.007843, (300, 300), 127.5)

  net.setInput(blob)
  detections = net.forward()

  """
  Detections is an array of shape [1, 1, 100, 7]
  The inner-most element is a 1D array of size 7. In this innermost array(call it arr),
  arr[1] represents the index of the label which can be found in the CLASSES array(CLASSES[arr[1]]). 
  arr[2] represents the confidence score as 0<x<1. 
  arr[3:7] represent bounding box coordinates represented as (x1, y1) and (x2, y2). 
  These coordinates have to be scaled up by the width and height of the original image.
  """
  
  for i in np.arange(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.25:
      idx = int(detections[0, 0, i, 1])
      label = CLASSES[idx]
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      print(box)
