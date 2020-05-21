import time
import cv2
import sys
import numpy as np
from picameravideostream import PiCameraVideoStream
from fps import FPS
from keyboard_thread import KeyboardThread

# Setting a global variable which will be edited by the keyboard_press_event_callback
# when the user presses 'q'. Need to find an alternative to a global variable
user_exit = False

# This method is used as a callback for when the user presses a key
def keyboard_press_event_callback(inp):
  if inp == 'q':
    global user_exit
    user_exit = True

# Setting this to output full numpy array and not truncated form
np.set_printoptions(threshold=sys.maxsize)

# Set of classes that OpenCV is set up to detect as an object
LABELS = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Set of labels that need to be ignored by the classifier
FILTERED_LABELS = [label for label in LABELS if label != "person"]

# Generate a random color in each class
COLORS = np.random.uniform(0, 255, size=(len(LABELS), 3))

# Load the caffe model and prototxt file
net = cv2.dnn.readNetFromCaffe(
    "model/MobileNetSSD_deploy.prototxt.txt", "model/MobileNetSSD_deploy.caffemodel")

# 1. Start the video stream, and the keyboard listener thread
# 2. Start the fps listener
# 3. Sleep for 2s to allow camera sensor to warm up
video_stream = PiCameraVideoStream().start()
kthread = KeyboardThread(keyboard_press_event_callback)
kthread.daemon = True # Setting this thread to be a daemon so it exits when the main program exits. This may not be a good idea.
kthread.startThread()
fps = FPS().start()

print("Warming up sensor")
time.sleep(2.0)
print("Starting loop")
while not user_exit:
  frame = video_stream.read()

  # This frame has the shape (240, 320, 3) which implies that there are 240 rows
  # each row has a set of 320 arrays and the inner most value is the RGB value of a
  # particular pixel
  (h, w) = frame.shape[:2]
  resized_frame = cv2.resize(frame, (300, 300))
  blob = cv2.dnn.blobFromImage(
      resized_frame, 0.007843, (300, 300), 127.5)
  net.setInput(blob)
  detections = net.forward()
  fps.update()

  """
  Detections is an array of shape [1, 1, 100, 7]
  The inner-most element is a 1D array of size 7. In this innermost array(call it arr),
  arr[1] represents the index of the label which can be found in the LABELS array(LABELS[arr[1]]). 
  arr[2] represents the confidence score as 0<x<1. 
  arr[3:7] represent bounding box coordinates represented as (x1, y1) and (x2, y2). 
  These coordinates have to be scaled up by the width and height of the original image.
  """

  for i in np.arange(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.25:
        idx = int(detections[0, 0, i, 1])
        label = LABELS[idx]
        if label in FILTERED_LABELS:
          continue
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        centroid_x = (box[0] + box[2]) / 2
        centroid_y = (box[1] + box[3]) / 2
        print(w, h)
        print(label)
        print(box)

# Stop all external modules and clean up threads
fps.stop()
kthread.stop()
video_stream.stop()
