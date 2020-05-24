from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

"""
This class is used to start the piCamera and run a separate thread to obtain frames from it.
"""
class PiCameraVideoStream:
  def __init__(self, resolution=(320, 240), framerate=30):
    self.camera = PiCamera()
    self.camera.resolution = resolution
    self.camera.framerate = framerate
    self.rawCapture = PiRGBArray(self.camera, size=resolution)
    self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port="True")
    self.frame = None
    self.stopped = False

  def start(self):
    Thread(target=self.update, args=()).start()
    return self

  def update(self):
    for f in self.stream:
      self.frame = f.array
      self.rawCapture.truncate(0)

      if self.stopped:
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.frame = None
        return

  def read(self):
    return self.frame

  def stop(self):
    self.stopped = True