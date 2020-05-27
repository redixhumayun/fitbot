from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import time
import numpy as np


class ServoClass:
  def __init__(self, servo_pin=18):
    self.factory = PiGPIOFactory()
    self.servo_pin = servo_pin
    self.servo = Servo(servo_pin, pin_factory=self.factory)

  def rotate(self, pid_output, image_width):
    value = pid_output.value
    interpolation_result = self.get_interpolation_result(value, image_width)
    self.servo.value = interpolation_result
    
  def get_interpolation_result(self, pid_output, image_width):
    # Setting the input range to be -(image/width / 2) < x < (image_width / 2)
    return np.interp(pid_output, [-(image_width / 2), (image_width / 2)], [-1, 1])