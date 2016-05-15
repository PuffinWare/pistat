import logging
import random
import threading
import time

import onewire

log = logging.getLogger(__name__)

# ROM Commands
ROM_ALARM_SEARCH = 0xEC

# Config Values
CFG_9_BIT = 0x1F
CFG_10_BIT = 0x3F
CFG_11_BIT = 0x5F
CFG_12_BIT = 0x7F

# Commands
CMD_CONVERT_TEMP = 0x44
CMD_READ_SCRATCH = 0xBE
CMD_WRITE_SCRATCH = 0x4E
CMD_COPY_SCRATCH = 0x48
CMD_RECALL_E2 = 0xb8
CMD_READ_POWER = 0xB4

# Default values for alarms in 9-bit values
DEG_100_9_BIT = 0xC8
DEG_0_9_BIT = 0x00

class DS18B20(object):
  def __init__(self, ds2482, address=None, channel=0, resolution=CFG_12_BIT):
    self.ds2482 = ds2482
    self.address = address
    self.channel = channel
    self.degc = 0
    self.degf = 0

    # TODO: if address, use match rom and the 8 byte address
    # data = [onewire.ROM_SKIP, CMD_WRITE_SCRATCH, DEG_100_9_BIT, DEG_0_9_BIT, resolution]
    # self.ds2482.execute(event.WriteTo1W(data, channel=self.channel))
    # data = [onewire.ROM_SKIP, CMD_COPY_SCRATCH]
    # self.ds2482.execute(event.WriteTo1W(data, channel=self.channel))

  def update(self):
    t = threading.Thread(target=self.run)
    t.start()

  def run(self):
    log.debug('Acquiring Temp')
    # TODO: if address, use match rom and the 8 byte address
    self.exec_and_wait(onewire.WriteTo1W([onewire.ROM_SKIP, CMD_CONVERT_TEMP], channel=self.channel))
    time.sleep(0.75)
    self.exec_and_wait(onewire.WriteTo1W([onewire.ROM_SKIP, CMD_READ_SCRATCH], channel=self.channel))
    read_msg = onewire.ReadFrom1W(9, reset=False, channel=self.channel)
    self.exec_and_wait(read_msg)

    data = read_msg.data
    for i in range(0, 2):
      log.debug('Rsp: %s | %s', hex(data[i]), bin(data[i]))
    lsb = data[0]
    msb = data[1] << 8
    reading = lsb | msb
    self.degc = reading * 0.0625
    self.degf = ((reading * 0.5625) / 5) + 32
    log.debug('Temp: %d | %.2fF | %.2fC', reading, self.degf, self.degc)

  def exec_and_wait(self, msg):
    self.ds2482.execute(msg)
    msg.join()

class DS18B20_SIM(object):
  def __init__(self, temp=70.0, variance=1.0):
    self.temp = temp
    self.degf = temp
    self.degc = ((self.degf * 9) / 5) - 32
    self.variance = variance

  def update(self):
    t = threading.Thread(target=self.run)
    t.start()

  def run(self):
    log.debug('Simulating DS18B20')
    time.sleep(0.75)
    rnd = float(int((random.uniform(0, self.variance*2) - self.variance) * 100)) / 100
    self.degf = self.temp + rnd
    log.debug('Temp: %.2fF | %.2fC', self.degf, self.degc)
