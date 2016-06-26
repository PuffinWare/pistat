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
  sensor = ForeignKeyField(Sensor, on_delete='CASCADE')
  created = DateTimeField(default=datetime.now)
  reading = FloatField()

class Alert(object):
  def __init__(self, level, title, message):
    self.level = level
    self.title = title
    self.message = message
