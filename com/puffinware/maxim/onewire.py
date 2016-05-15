import threading

# ROM Commands
ROM_SEARCH = 0xF0
ROM_READ = 0x33
ROM_MATCH = 0x55
ROM_SKIP = 0xCC

class Status(object):
  def __init__(self, status_byte):
    self.oneWireBusy = (status_byte & 0x01) == 0x01
    self.presencePulse = (status_byte & 0x02) == 0x02
    self.shortDetected = (status_byte & 0x04) == 0x04
    self.logicLevel = (status_byte & 0x08) == 0x08
    self.deviceReset = (status_byte & 0x10) == 0x10
    self.singleBitResult = (status_byte & 0x20) == 0x20
    self.tripletSecondBit = (status_byte & 0x40) == 0x40
    self.branchDirTaken = (status_byte & 0x80) == 0x80

class OneWireEvent(object):
  """
  Base Class for all 1Wire events
  """
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

SHUTDOWN = OneWireEvent(None)

class WriteTo1W(OneWireEvent):
  """
  Base Class for all 1Wire events
  """
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
