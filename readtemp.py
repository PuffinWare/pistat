#!/usr/bin/python

import logging, logging.handlers
from maxim.event import WriteTo1W,ReadFrom1W
from maxim import DS2482
import time

log = logging.getLogger(__name__)

def setup_logger(debug):
  logger = logging.getLogger()
  if debug:
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)
  formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", "%H:%M:%S")
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(formatter)
  logger.addHandler(consoleHandler)

def complete(data):
  log.info('complete')
  for i in range(0, 2):
    log.info('%s | %s', hex(data[i]), bin(data[i]))
  lsb = data[0]
  msb = data[1] << 8
  reading = lsb | msb
  degc = reading * 0.0625
  degf = ((reading * 0.5625) / 5) + 32
  log.info('%d | %.2f | %.2f', reading, degc, degf)

setup_logger(False)
log.info('Start')
ds = DS2482()

# Initate temp conversion
for chn in range(0, 3):
  ds.handle_event(WriteTo1W('\xCC\x44', channel=chn))
# Wait 750ms for conversion to complete
  time.sleep(0.75)
# Read values
for chn in range(0, 3):
  log.info("-- %d --", chn)
  ds.handle_event(WriteTo1W('\xCC\xBE', channel=chn))
  read = ReadFrom1W(9, reset=False, channel=chn)
  ds.handle_event(read)
  read.join()
  complete(read.data)

log.info('Done')
