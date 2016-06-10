from com.puffinware.pistat.models import Category,Alert,NavHelper
from flask import render_template, request
from logging import getLogger

log = getLogger(__name__)

def setup_routes(app, **kwargs):

  # The "entry" point
  @app.route('/termostat')
  def thermostat():
    return render_template('index.html', nav=nav_helper(NavHelper.HOME))

