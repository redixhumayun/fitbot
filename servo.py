import RPi.GPIO as GPIO
import numpy as np
import time

# Set up the correct GPIO pin number the servo is connected to
# Set the pin numbering mode of the Pi to Broadcom mode
# Set up the pin as an output
servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Set up the duty cycle values of the servo between 2 and 10
control = np.linspace(4, 8, num = 20)

# Set up the servo pin as a PWM pin and specify the duty cycle
p = GPIO.PWM(servo_pin, 50)
p.start(0)

# Run a loop changing the duty cycle supplied by the servo pin to watch it rotate
try:
  while True:
    for x in control:
      print(x)
      p.ChangeDutyCycle(x)
      time.sleep(0.5)
    
    for x in reversed(control):
      print(x)
      p.ChangeDutyCycle(x)
      time.sleep(0.5)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()