import threading

class OneWireEvent(object):
  def __init__(self, channel=None, reset=True, callback=None, delay=0):
    self.channel = channel
    self.reset = reset
    self.callback = callback
    self.delay = delay
    self.failed = None
    self.lock = threading.Event()

  def join(self):
    self.lock.wait()
    if self.failed is not None:
      raise self.failed[0], self.failed[1], self.failed[2]

  def fail(self, exc_info):
    self.failed = exc_info
    self.lock.set()

class WriteTo1W(OneWireEvent):
  def __init__(self, data, **kwargs):
    OneWireEvent.__init__(self, **kwargs)
    self.data = data

  def complete(self):
    self.lock.set()

class ReadFrom1W(OneWireEvent):
  def __init__(self, count, **kwargs):
    OneWireEvent.__init__(self, **kwargs)
    self.count = count

  def complete(self, data):
    self.data = data
    self.lock.set()
