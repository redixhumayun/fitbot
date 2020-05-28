from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
import time
import numpy as np


class ServoClass:
  def __init__(self, servo_pin=12):
    self.factory = PiGPIOFactory()
    self.servo_pin = servo_pin
    self.servo = gpiozero.Servo(servo_pin, pin_factory=self.factory)
    self.last_position = 0
    self.moving = False
    self.rotate(0)

  def rotate(self, pid_output):
    self.servo.value = 0
    # while self.servo.value < 0.95:
    #   self.servo.value += 0.05
    #   print(self.servo.value)
    #   time.sleep(0.5)

servo = ServoClass()