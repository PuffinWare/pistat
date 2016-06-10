"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from peewee import Model, CharField, IntegerField, FloatField, DateTimeField, PrimaryKeyField, ForeignKeyField
from datetime import datetime
from com.puffinware.pistat import DB

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
  category = ForeignKeyField(Category, null=True)
  status = IntegerField(default=Status.ACTIVE)
  name = CharField()
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

class Sensor(BaseModel):
  id = PrimaryKeyField()
  category = ForeignKeyField(Category, null=True)
  thermostat = ForeignKeyField(Thermostat, null=True)
  name = CharField()
  sensor_type = CharField()
  status = IntegerField(default=Status.ACTIVE)
  created = DateTimeField(default=datetime.now)
  modified = DateTimeField(default=datetime.now)

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