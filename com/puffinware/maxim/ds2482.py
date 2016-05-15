import smbus
import time, sys
import Queue
import logging
from onewire import Status,SHUTDOWN,ReadFrom1W,WriteTo1W
from threading import Thread

log = logging.getLogger(__name__)

# Commands
CMD_DEVICE_RESET    = 0xF0
CMD_SET_READ_PTR    = 0xE1
CMD_WRITE_CONFIG    = 0xD2
CMD_CHANNEL_SELECT  = 0xC3
CMD_1W_RESET        = 0xB4
CMD_1W_SINGLE_BIT   = 0x87
CMD_1W_WRITE_BYTE   = 0xA5
CMD_1W_READ_BYTE    = 0x96
CMD_1W_TRIPLET      = 0x78

# Registers
REG_STATUS      = 0xF0
REG_READ_DATA   = 0xE1
REG_CHANNEL_SEL = 0xD2
REG_CONFIG      = 0xC3

# Channel Codes
CHANNELS = {
  0: 0xF0,
  1: 0xE1,
  2: 0xD2,
  3: 0xC3,
  4: 0xB4,
  5: 0xA5,
  6: 0x96,
  7: 0x87
}

class DS2482(Thread):
  def __init__(self, address=0x18, bus=None):
    Thread.__init__(self)
    self.address = address
    self.queue = Queue.Queue()
    self.i2cbus = bus if bus is not None else smbus.SMBus(1)
    self.shutdown = False
    self.start()

  def execute(self, event):
    self.queue.put(event)

  def stop(self):
    self.queue.put(SHUTDOWN)

  def run(self):
    while True:
      event = None
      try:
        event = self.queue.get(1000)
        if event is SHUTDOWN:
          break
        log.debug('Event: %s', type(event).__name__)
        self.handle_event(event)
        log.debug('Complete: %s', type(event).__name__)

      except Queue.Empty:
        continue

      except:
        event.fail(sys.exc_info())

    self.i2cbus.close()

  def handle_event(self, event):
    if event.channel is not None:
      log.debug('channelsel: %d | %s', event.channel, hex(CHANNELS[event.channel]))
      self.i2cbus.write_byte_data(self.address, CMD_CHANNEL_SELECT, CHANNELS[event.channel])

    if event.reset:
      log.debug('1w-reset')
      self.i2cbus.write_byte(self.address, CMD_1W_RESET)
      self.poll_1w_busy()

    if type(event) is WriteTo1W:
      self.write_to_1w(event)
    elif type(event) is ReadFrom1W:
      self.read_from_1w(event)

    if event.delay > 0:
      time.sleep(event.delay)

  def poll_1w_busy(self):
    while True:
      log.debug('poll1w')
      time.sleep(0.001) # Just pause a bit to let 1W comm finish, usually < 1ms
      status = self.read_status()
      if not status.oneWireBusy:
        break

  def config(self, active_pullup=True, strong_pullup=False, onewire_speed=False):
    cfg = 0x00
    cfg |= 0x01 if active_pullup else 0x00
    cfg |= 0x04 if strong_pullup else 0x00
    cfg |= 0x08 if onewire_speed else 0x00
    cfg |= (~cfg << 4)

  def read_status(self, set_ptr=False):
    if set_ptr:
      self.i2cbus.write_byte_data(self.address, CMD_SET_READ_PTR, REG_STATUS)

    temp_status = self.i2cbus.read_byte(self.address)
    log.debug('Status: %s', bin(temp_status))

    return Status(temp_status)

  def read_byte(self):
    self.i2cbus.write_byte_data(self.address, CMD_SET_READ_PTR, REG_READ_DATA)
    byte = self.i2cbus.read_byte(self.address)
    log.debug('Read: %s | %s', hex(byte), bin(byte))
    return byte

  def write_to_1w(self, event):
    """
    Write one or more bytes of data out to a 1W device
    """
    for char in event.data:
      byte = char
      # byte = ord(char)
      log.debug('1w-write: %s | %s', hex(byte), bin(byte))
      self.i2cbus.write_byte_data(self.address, CMD_1W_WRITE_BYTE, byte)
      self.poll_1w_busy()

    event.complete()

  def read_from_1w(self, event):
    """
    Read bytes of data from a 1W device
    """
    data = []
    for i in range(0, event.count):
      log.debug('1w-read')
      self.i2cbus.write_byte(self.address, CMD_1W_READ_BYTE)
      self.poll_1w_busy()
      data.append(self.read_byte())

    event.complete(data)
