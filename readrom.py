#!/usr/bin/python

import sys
import logging, logging.handlers
import maxim.event
from maxim import DS2482

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
    for char in data:
      log.info('%s | %s', hex(char), bin(char))

  def fail(self):
    log.error('fail')

setup_logger(False)
log.info('Start')
ds = DS2482()

chn = int(sys.argv[1])

ds.handle_event(maxim.event.WriteTo1W('\x33', channel=chn))
ds.handle_event(maxim.event.ReadFrom1W(8, reset=False, channel=chn, callback=Callback()))

log.info('Done')
