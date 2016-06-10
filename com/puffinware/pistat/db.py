"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from com.puffinware.pistat.models import User, Location, Category, Thermostat, Sensor, Reading
from com.puffinware.pistat import DB
from logging import getLogger

log = getLogger(__name__)

def setup_db(app):
  DB.create_tables([User, Location, Category, Thermostat, Sensor, Reading], safe=True)

  # This hook ensures that a connection is opened to handle any queries
  # generated by the request.
  @app.before_request
  def _db_connect():
    log.debug('DB Connect')
    DB.connect()

  # This hook ensures that the connection is closed when we've finished
  # processing the request.
  @app.teardown_request
  def _db_close(exc):
    if not DB.is_closed():
      log.debug('DB Close')
      DB.close()