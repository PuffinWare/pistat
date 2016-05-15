#!/usr/bin/python

import logging
import logging.handlers
import time

from maxim import DS2482,DS18B20

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

setup_logger(False)
log.info('Start')
ds = DS2482()
ds.start()

sensors = [
  DS18B20(ds, channel=0),
  DS18B20(ds, channel=1),
  DS18B20(ds, channel=2)
]

# Initate temp conversion
for i in range(0, 3):
  sensors[i].update()

time.sleep(1)

# Read values
for i in range(0, 3):
  log.info('%.2f | %.2f', sensors[i].degc, sensors[i].degf)

ds.stop()
log.info('Done')
