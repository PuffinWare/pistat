from com.puffinware.pistat.models import Sensor,Alert,NavHelper,SensorHelper
from flask import render_template, request, redirect, url_for
from logging import getLogger
import json

log = getLogger(__name__)

def setup_routes(app, **kwargs):

  @app.route('/config/sensor', methods=['POST', 'GET'])
  def sensor_main():
    if request.method == "GET": # Empty form
      cid = request.args.get('category_id', '')
      tid = request.args.get('thermostat_id', '')
      return render_template('edit_sensor.html', category_id=cid, thermostat_id=tid, sh=SensorHelper(None), nav=NavHelper(NavHelper.CONFIG))

    # Create new or update existing
    sid = request.form.get('sensor_id', None)
    tid = request.form.get('thermostat_id', None)
    cid = request.form.get('category_id', None)
    log.debug('save sensor: %s | c:%s | t:%s', sid, cid, tid)
    if sid is None:
      sensor = Sensor(category=cid, thermostat=tid, sh=SensorHelper(None))
    else:
      sensor = Sensor.get(Sensor.id == sid)

    sensor.name = request.form.get('sensor_name')
    sensor.sensor_type = request.form.get('sensor_type')
    config = {
      'address': request.form.get('sensor_address'),
      'channel': request.form.get('sensor_channel')
    }
    sensor.config = json.dumps(config, indent=2)
    sensor.save()
    return redirect(url_for('config'))

  @app.route('/config/sensor/<sensor_id>', methods=['GET'])
  def sensor_load(sensor_id):
    sensor = Sensor.get(Sensor.id == sensor_id)
    return render_template('edit_sensor.html', sensor=sensor, sh=SensorHelper(sensor), nav=NavHelper(NavHelper.CONFIG))

  @app.route('/config/sensor/<sensor_id>/delete', methods=['GET'])
  def sensor_delete(sensor_id):
    log.debug('delete sensor: %s', sensor_id)
    sensor = Sensor.get(Sensor.id == sensor_id)
    sensor.delete_instance()
    return redirect(url_for('config'))