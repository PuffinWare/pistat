"""
Copyright 2016 Puffin Software. All rights reserved.
"""
from com.puffinware.pistat.models import NavHelper,NavLocation
from flask import render_template, request
from logging import getLogger

log = getLogger(__name__)

def setup_routes(app, **kwargs):

  # The "entry" point
  @app.route('/')
  def index():
    return render_template('index.html', nav=nav_helper(NavLocation.HOME))

  @app.route('/config')
  def config():
    return render_template('config.html', nav=nav_helper(NavLocation.CONFIG))

  def nav_helper(loc):
    return NavHelper(loc)
