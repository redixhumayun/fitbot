import threading

"""
This class listens for keyboard input events on a separate thread using the input() function.
It calls a callback function in the main python class to indicate a pressed key
"""
class KeyboardThread(threading.Thread):
  def __init__(self, input_callback=None, name='keyboard-input-thread'):
    self.input_callback = input_callback
    self.stopped = False
    super(KeyboardThread, self).__init__(name=name)
  
  def startThread(self):
    self.start()

  def run(self):
    while True:
      self.input_callback(input())
      if self.stopped:
        break
  
  def stop(self):
    self.stopped = True