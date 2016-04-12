#!/usr/bin/python

import logging, logging.handlers
import ds2482.event
import ds2482.ds2482
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

class Callback(object):
  def complete(self, data):
    log.info('complete')
    for i in range(0, 2):
      log.info('%s | %s', hex(data[i]), bin(data[i]))
    lsb = data[0]
    msb = data[1] << 8
    reading = lsb | msb
    degc = reading *0.0625
    degf = ((reading * 0.5625) / 5) + 32
    log.info('%d | %.2f | %.2f', reading, degc, degf)

  def fail(self):
    log.error('fail')

setup_logger(False)
log.info('Start')
ds = ds2482.ds2482.DS_2482()

# for chn in range(0, 3):
#   log.info("-- %d --", chn)
#   ds.handle_event(ds2482.event.WriteTo1W('\xCC\x44', channel=chn, delay=0.75))
#   ds.handle_event(ds2482.event.WriteTo1W('\xCC\xBE', channel=chn))
#   ds.handle_event(ds2482.event.ReadFrom1W(9, reset=False, channel=chn, callback=Callback()))

# Initate temp conversion
for chn in range(0, 3):
  ds.handle_event(ds2482.event.WriteTo1W('\xCC\x44', channel=chn))
# Wait 750ms for conversion to complete
time.sleep(0.75)
# Read values
for chn in range(0, 3):
  log.info("-- %d --", chn)
  ds.handle_event(ds2482.event.WriteTo1W('\xCC\xBE', channel=chn))
  ds.handle_event(ds2482.event.ReadFrom1W(9, reset=False, channel=chn, callback=Callback()))

log.info('Done')
