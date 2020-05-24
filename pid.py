import time

"""
A class that will implement a PID controller that will help control the direction and travel
of the pan/tilt mechanism using servo controls
"""

class PID:
  def __init__(self, kP=1, kI=0, kD=0):
    # Initialize the k values for the controller
    self.kP = kP
    self.kI = kI
    self.kD = kD
    self.initialize()

  def initialize(self):
    # Initialize the time, error and coefficient terms
    self.currTime = time.time()
    self.prevTime = self.currTime
    self.prevError = 0
    self.cP = 0
    self.cI = 0
    self.cD = 0

  def update(self, error):
    # Setting a sleep time of a higher value delays the camera's response,
    # but it allows the servo to respond accurately to the new frame being provided
    time.sleep(0.75)

    # Update the time and calculate delta of time and error
    self.currTime = time.time()
    deltaTime = self.currTime - self.prevTime
    deltaError = error - self.prevError
    
    # Calculate the coefficient of the proportional term
    self.cP = error

    # Calculate the coefficient of the integral term
    self.cI = error * deltaTime

    # Calculate the coefficient of the derivative term
    self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

    self.prevTime = self.currTime
    self.prevError = error

    return sum([self.kP * self.cP, self.kI * self.cI, self.kD * self.cD])