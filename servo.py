import RPi.GPIO as GPIO
import numpy as np
import time

class Servo:
  def __init__(self, servo_pin=17):
    self.servo_pin = servo_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.servo_pin, GPIO.OUT)
    self.pwm = GPIO.PWM(self.servo_pin, 50)
    self.pwm.start(0)

  def rotate(self, pid_output, image_width):
    value = pid_output.value
    interpolation_result = self.get_interpolation_result(value, image_width)
    print(interpolation_result)
    # self.pwm.ChangeDutyCycle(interpolation_result)

  def get_interpolation_result(self, pid_output, image_width):
    # Setting the input range to be -(image/width / 2) < x < (image_width / 2)
    return np.interp(pid_output, [-(image_width / 2), (image_width / 2)], [2, 10])

  def stop(self):
    self.pwm.stop()
    GPIO.cleanup()