"""
Copyright 2016 Puffin Software. All rights reserved.
"""
from logging import getLogger
import json

log = getLogger(__name__)

class NavHelper(object):
  HOME = 1
  CONFIG = 2

  def __init__(self, location):
    self.location = location

  def nav_home(self):
    return self.location == NavHelper.HOME

  def nav_config(self):
    return self.location == NavHelper.CONFIG

class SensorHelper(object):
  def __init__(self, sensor):
    self.sensor = sensor
    self.channels = map(str, range(0, 8))
    self.addresses = map(hex, range(24, 32))
    if sensor is not None:
      self.config = json.loads(sensor.config)

  def sensor_type(self, check):
    return self.output(self.sensor is not None and self.sensor.sensor_type == check)

  def address(self, check):
    return self.output(self.sensor is not None and self.config['address'] == check)

  def channel(self, check):
    return self.output(self.sensor is not None and self.config['channel'] == str(check))

  def output(self, condition):
    return ' selected="selected"' if condition else ''