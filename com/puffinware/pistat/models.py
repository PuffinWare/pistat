"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from peewee import Model, CharField, IntegerField, FloatField, DateTimeField, PrimaryKeyField, ForeignKeyField
from datetime import datetime
from com.puffinware.pistat import DB
import json

class Status(object):
  ACTIVE = 1
  DISABLED = 1

class BaseModel(Model):
    class Meta:
        database = DB

class User(BaseModel):
  id = PrimaryKeyField()
  name = CharField()
  email = CharField()
  phone = CharField()

class Location(BaseModel):
  id = PrimaryKeyField()
  name = CharField()
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

class Category(BaseModel):
  id = PrimaryKeyField()
  name = CharField()
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

class Thermostat(BaseModel):
  id = PrimaryKeyField()
  category = ForeignKeyField(Category, null=True, on_delete='CASCADE')
  status = IntegerField(default=Status.ACTIVE)
  name = CharField()
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

class Sensor(BaseModel):
  id = PrimaryKeyField()
  category = ForeignKeyField(Category, null=True, on_delete='CASCADE')
  thermostat = ForeignKeyField(Thermostat, null=True, on_delete='CASCADE')
  name = CharField()
  sensor_type = CharField()
  status = IntegerField(default=Status.ACTIVE)
  config = CharField()
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

class SensorType(BaseModel):
  id = PrimaryKeyField()
  sensor_type = CharField()
  sensor_desc = CharField()

class Reading(BaseModel):
  id = PrimaryKeyField()
  sensor = ForeignKeyField(Sensor)
  created = DateTimeField(default=datetime.now)
  reading = FloatField()

class Alert(object):
  def __init__(self, level, title, message):
    self.level = level
    self.title = title
    self.message = message

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
    return self.output(self.sensor is not None and self.type == check)

  def address(self, check):
    return self.output(self.sensor is not None and self.config['address'] == check)

  def channel(self, check):
    return self.output(self.sensor is not None and self.config['channel'] == str(check))

  def output(self, condition):
    return ' selected="selected"' if condition else ''