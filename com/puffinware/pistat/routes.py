"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from com.puffinware.pistat.models import Category
from com.puffinware.pistat.helpers import NavHelper
from com.puffinware.pistat.dao.reading_dao import current_readings
from flask import render_template, request
from logging import getLogger
import category, thermostat, sensor

log = getLogger(__name__)

def setup_routes(app, **kwargs):
  ## Setup the common routes here

  # The "entry" point
  @app.route('/')
  def index():
    categories = Category.select()
    if len(categories) == 0:
      return render_template('empty.html', nav=NavHelper(NavHelper.HOME))
    readings = current_readings()
    return render_template('index.html', categories=categories, readings=readings, nav=NavHelper(NavHelper.HOME))

  @app.route('/config')
  def config():
    categories = Category.select()
    # for c in categories:
    #   log.debug('%d stats in %s', len(c.thermostat_set), c.name)
    return render_template('config.html', categories=categories, nav=NavHelper(NavHelper.CONFIG))

  ## Setup all the module's routes
  category.setup_routes(app)
  thermostat.setup_routes(app)
  sensor.setup_routes(app)