from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
import time
import numpy as np
import math

class ServoClass:
  def __init__(self, servo_pin=18):
    self.factory = PiGPIOFactory()
    self.servo_pin = servo_pin
    self.servo = gpiozero.Servo(servo_pin, pin_factory=self.factory)

  def rotate(self, pid_output):
    # Only print out if value is not 0
    if math.isclose(0, pid_output) is False:
      print("pid_output: ", pid_output)
    # diff = self.last_position - pid_output
    diff = 0 - pid_output
    # Only print out if value is not 0
    if math.isclose(0, diff) is False:
      print("diff: ", diff)

    # This margin of error is acceptable
    if  diff < 0.05 and diff > -0.05:
      return

    
    if diff > 0:
      # Rotate clockwise
      while diff > 0:
        print('Rotating clockwise')
        try:
          self.servo.value -= 0.025
          print("servo_value: ", self.servo.value)
        except gpiozero.exc.OutputDeviceBadValue:
          print('Bad value')
          pass

        diff -= 0.025
      time.sleep(1)
      
    elif diff < 0:
      # Rotate counter-clockwise
      while diff < 0:
        print('Rotating counter-clockwise')
        try: 
          self.servo.value += 0.025
          print("servo_value: ", self.servo.value)
        except gpiozero.exc.OutputDeviceBadValue:
          print('Bad value')
          pass

        diff += 0.025
      time.sleep(1)

  def move_servo_to_position(self, pid_output):
    if self.moving is True:
      # Servo is already currently moving
      return
    self.rotate(pid_output)
  # def rotate(self, pid_output):
  #   # interpolation_result = self.get_interpolation_result(value, image_width)
  #   try:
  #     self.servo.value = pid_output
  #   except gpiozero.exc.OutputDeviceBadValue:
  #     print('Bad value provided')