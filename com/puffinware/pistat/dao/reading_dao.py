"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from com.puffinware.pistat.models import Sensor,Reading
from logging import getLogger

log = getLogger(__name__)

def current_readings():
  sensors = Sensor.select()
  readings = {}
  for s in sensors:
    query = Reading.select()\
      .join(Sensor)\
      .where(Sensor.id == s.id)\
      .order_by(-Reading.created)\
      .limit(1)
    try:
      reading = query.execute().next()
      readings[s.id] = reading.reading
    except StopIteration:
      log.debug('No reading for sensor: %d|%s', s.id, s.name)
      pass

  log.debug('Readings %s', readings)
  return readings

def get_readings_for_sensor(self, sensor_id):
  pass
