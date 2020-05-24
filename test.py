import time
import cv2
import sys
import numpy as np
from multiprocessing import Process
from multiprocessing import Manager
import signal
from picameravideostream import PiCameraVideoStream
from fps import FPS
from pid import PID
from servo import Servo

# Define the resolution
resolution=(480, 368)

# create the servo instance
servo = Servo()

def signal_handler(sig, frame):
  print('Performing clean up before exit!')

  # Perform clean up before exit
  servo.stop()
  cv2.destroyAllWindows()

  print('Done cleaning up...')
  sys.exit(0)

def detect_obj_center(resolution, pan):
  signal.signal(signal.SIGINT, signal_handler)

  # Set of classes that OpenCV is set up to detect as an object
  LABELS = ["background", "aeroplane", "bicycle", "bird", "boat",
          "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
          "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
          "sofa", "train", "tvmonitor"]

  # Set of labels that need to be ignored by the classifier
  FILTERED_LABELS = [label for label in LABELS if label != "person"]

  # Load the caffe model and prototxt file
  net = cv2.dnn.readNetFromCaffe(
    "model/MobileNetSSD_deploy.prototxt.txt", "model/MobileNetSSD_deploy.caffemodel")

  #	1. Start video stream
  #	2. Initialize the PID class
  #	3. Initialize the FPS class
  video_stream = PiCameraVideoStream(resolution=resolution).start()
  pid_instance = PID(0.12, 0.05, 0.0025)
  fps = FPS().start()

  print("Warming up sensor")
  time.sleep(2.0)
  print("Starting loop")

  while True:
    try:
      frame = video_stream.read()

      # This frame has the shape (720, 1280, 3) which implies that there are 720 rows
      # each row has a set of 1280 arrays and the inner most value is the RGB value of a
      # particular pixel
      (h, w) = frame.shape[:2]
      image_center_x = w / 2
      image_center_y = h / 2
      blob = cv2.dnn.blobFromImage(cv2.resize(
          frame, (300, 300)), 0.007843, (300, 300), 127.5)
      net.setInput(blob)
      detections = net.forward()

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
          (startX, startY, endX, endY) = box.astype("int")
          cv2.rectangle(frame, (startX, startY),
                        (endX, endY), (255, 0, 0), 2)
          centroid_x = (box[0] + box[2]) / 2
          centroid_y = (box[1] + box[3]) / 2
          # print("**********************************")
          # print("centroid: ", centroid_x, centroid_y)
          error_x = image_center_x - centroid_x
          error_y = image_center_y - centroid_y
          result = pid_instance.update(error_x)
          pan.value = result
          # servo.rotate(result, w)
          # print(label)
          # print(box)
          # print(result)

      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF
      fps.update()
    except (KeyboardInterrupt, SystemExit):
      break

  # Stop all external modules and clean up threads
  print("Stopping object detection process")
  fps.stop()

def run_servos(pan, tilt, image_width):
  signal.signal(signal.SIGINT, signal_handler)
  while True:
    try:
      servo.rotate(pan, image_width)
    except (KeyboardInterrupt, SystemExit):
      break
  
if __name__ == "__main__":
  # Start a multi-processing manager that will allow variable sharing between processes
  with Manager() as manager:
    #	Set values for pan and tilt
    pan = manager.Value("d", 0.0)
    tilt = manager.Value("d", 0.0)

    #	Create a processes list
    processes = []

    #	Start a process for:
    #	1. Object detection
    #	2. Servo rotation
    processDetectObjCenter = Process(target=detect_obj_center, args=(resolution, pan))
    processes.append(processDetectObjCenter)
    processRunServos = Process(target=run_servos, args=(pan, tilt, resolution[1]))
    processes.append(processRunServos)

    #	Start all processes
    for process in processes:
      process.start()

    #	Join all processes
    for process in processes:
      process.join()