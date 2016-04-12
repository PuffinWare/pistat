#!/usr/bin/python

import logging, logging.handlers
import ds2482.event
import ds2482.ds2482

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
ds = ds2482.ds2482.DS_2482()

ds.handle_event(ds2482.event.WriteTo1W('\x33', channel=0))
ds.handle_event(ds2482.event.ReadFrom1W(8, reset=False, channel=0, callback=Callback()))

log.info('Done')
