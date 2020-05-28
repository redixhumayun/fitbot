from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
import time
import numpy as np
import math

class ServoClass:
  def __init__(self, servo_pin):
    self.factory = PiGPIOFactory()
    self.servo_pin = servo_pin
    self.servo = gpiozero.Servo(servo_pin, pin_factory=self.factory)

  def rotate(self, pid_output):
    # This calculation shouldn't be necessary
    # TODO: Remove the sign flip and change if conditions
    diff = 0 - pid_output

    # This margin of error is acceptable
    if  diff < 0.05 and diff > -0.05:
      return

    
    if diff > 0:
      # Rotate clockwise
      while diff > 0:
        try:
          self.servo.value -= 0.025
        except gpiozero.exc.OutputDeviceBadValue:
          print('Bad value')
          pass

        diff -= 0.025
      time.sleep(1)
      
    elif diff < 0:
      # Rotate counter-clockwise
      while diff < 0:
        try: 
          self.servo.value += 0.025
        except gpiozero.exc.OutputDeviceBadValue:
          print('Bad value')
          pass

        diff += 0.025
      time.sleep(1)