"""
Copyright 2016 Puffin Software. All rights reserved.
"""

from com.puffinware.pistat.models import Category,Alert,NavHelper
from flask import render_template, request
from logging import getLogger
import category, thermostat, sensor

log = getLogger(__name__)

def setup_routes(app, **kwargs):
  ## Setup the common routes here

  # The "entry" point
  @app.route('/')
  def index():
    return render_template('index.html', nav=nav_helper(NavHelper.HOME))

  @app.route('/config')
  def config():
    categories = Category.select()
    # for c in categories:
    #   log.debug('%d stats in %s', len(c.thermostat_set), c.name)
    return render_template('config.html', categories=categories, nav=nav_helper(NavHelper.CONFIG))

  def nav_helper(loc):
    return NavHelper(loc)

  ## Setup all the module's routes
  category.setup_routes(app)
  thermostat.setup_routes(app)
  sensor.setup_routes(app)