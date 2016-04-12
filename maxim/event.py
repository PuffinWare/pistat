class OneWireEvent(object):
  def __init__(self, channel=None, reset=True, callback=None, delay=0):
    self.channel = channel
    self.reset = reset
    self.callback = callback
    self.delay = delay

  def fail(self, reason):
    self.reason = reason
    if self.callback is not None:
      self.callback.fail(reason)

class WriteTo1W(OneWireEvent):
  def __init__(self, data, **kwargs):
    OneWireEvent.__init__(self, **kwargs)
    self.data = data

  def complete(self):
    if self.callback is not None:
      self.callback.complete()

class ReadFrom1W(OneWireEvent):
  def __init__(self, count, **kwargs):
    OneWireEvent.__init__(self, **kwargs)
    self.count = count

  def complete(self, data):
    self.data = data
    if self.callback is not None:
      self.callback.complete(data)
