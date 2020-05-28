from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
import time
import numpy as np


class ServoClass:
  def __init__(self, servo_pin=18):
    self.factory = PiGPIOFactory()
    self.servo_pin = servo_pin
    self.servo = gpiozero.Servo(servo_pin, pin_factory=self.factory)
    self.last_position = 0
    self.moving = False
    self.rotate(0)

  def rotate(self, pid_output):
    while self.servo.value < 0.95:
      self.servo.value += 0.05
      print(self.servo.value)
      time.sleep(0.5)
    # for i in np.arange(0, 0.7, 0.05):
    #   print(i)
    #   self.servo.value = i
    #   time.sleep(0.5)

servo = ServoClass()