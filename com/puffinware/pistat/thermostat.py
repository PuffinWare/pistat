from com.puffinware.pistat.models import Category,Thermostat,Alert,NavHelper
from flask import render_template, request, redirect, url_for
from logging import getLogger

log = getLogger(__name__)

def setup_routes(app, **kwargs):

  @app.route('/config/thermostat', methods=['POST', 'GET'])
  def thermostat_main():
    if request.method == "GET": # Empty form
      cid = request.args.get('category_id', '')
      return render_template('edit_thermostat.html', category_id=cid, nav=NavHelper(NavHelper.CONFIG))

    # Create new or update existing
    tid = request.form.get('thermostat_id', None)
    if tid is None:
      cid = request.form.get('category_id', None)
      log.debug('save new thermostat for category: %s', cid)
      thermostat = Thermostat(category=cid)
    else:
      log.debug('save thermostat: %s', tid)
      thermostat = Thermostat.get(Thermostat.id == tid)

    thermostat.name = request.form['thermostat_name']
    thermostat.save()
    return redirect(url_for('config'))

  @app.route('/config/thermostat/<thermostat_id>', methods=['GET'])
  def thermostat_load(thermostat_id):
    thermostat = Thermostat.get(Thermostat.id == thermostat_id)
    return render_template('edit_thermostat.html', thermostat=thermostat, nav=NavHelper(NavHelper.CONFIG))

  @app.route('/config/thermostat/<thermostat_id>/delete', methods=['GET'])
  def thermostat_delete(thermostat_id):
    log.debug('delete thermostat: %s', thermostat_id)
    thermostat = Thermostat.get(Thermostat.id == thermostat_id)
    thermostat.delete_instance()
    return redirect(url_for('config'))
