import time
import cv2
import sys
import numpy as np
import arrow
from multiprocessing import Process
from multiprocessing import Manager
import signal
from picameravideostream import PiCameraVideoStream
from fps import FPS
from pid import PID
from servo import ServoClass
from objcenter import ObjCenter

def signal_handler(sig, frame):
  print('Performing clean up before exit!')

  # Perform clean up before exit
  cv2.destroyAllWindows()

  print('Done cleaning up...')
  sys.exit(0)


def detect_obj_center(objX, objY, centerX, centerY):
  # signal trap to handle keyboard interrupt
  signal.signal(signal.SIGINT, signal_handler)

  # start the video stream and wait for the camera to warm up
  # vs = VideoStream(usePiCamera=True).start()
  vs = PiCameraVideoStream().start()
  time.sleep(2.0)

  # initialize the object center finder
  obj = ObjCenter("model/haarcascade_frontalface_default.xml")

  # loop indefinitely
  while True:
    # grab the frame from the threaded video stream
    start_time = arrow.utcnow()

    frame = vs.read()

    # calculate the center of the frame as this is where we will
    # try to keep the object
    (H, W) = frame.shape[:2]
    centerX.value = W // 2
    centerY.value = H // 2

    # find the object's location
    objectLoc = obj.update(frame, (centerX.value, centerY.value))
    ((objX.value, objY.value), rect) = objectLoc

    time_difference = arrow.utcnow() - start_time
    # print(time_difference.total_seconds() * 1000)

    # extract the bounding box and draw it
    if rect is not None:
      (x, y, w, h) = rect
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
        2)

    # display the frame to the screen
    cv2.imshow("Pan-Tilt Face Tracking", frame)
    cv2.waitKey(1)

def run_servos(pan, tilt, image_width):
  signal.signal(signal.SIGINT, signal_handler)

  # create the servo instance
  servo = ServoClass()
  
  while True:
    servo.rotate(pan, image_width)
    
if __name__ == "__main__":
  # Start a multi-processing manager that will allow variable sharing between processes
  with Manager() as manager:
    #	Set values for pan and tilt
    pan = manager.Value("d", 0.0)
    tilt = manager.Value("d", 0.0)

    # set integer values for the object center (x, y)-coordinates
    centerX = manager.Value("i", 0)
    centerY = manager.Value("i", 0)

    # set integer values for the object's (x, y)-coordinates
    objX = manager.Value("i", 0)
    objY = manager.Value("i", 0)

    #	Create a processes list
    processes = []

    #	Start a process for:
    #	1. Object detection
    #	2. Servo rotation
    processDetectObjCenter = Process(target=detect_obj_center, args=(objX, objY, centerX, centerY))
    processes.append(processDetectObjCenter)
    # processRunServos = Process(target=run_servos, args=(pan, tilt, resolution[1]))
    # processes.append(processRunServos)

    #	Start all processes
    for process in processes:
      process.start()

    #	Join all processes
    for process in processes:
      process.join()