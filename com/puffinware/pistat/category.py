from com.puffinware.pistat.models import Category
from com.puffinware.pistat.helpers import NavHelper
from flask import render_template, request, redirect, url_for
from logging import getLogger

log = getLogger(__name__)

def setup_routes(app, **kwargs):

  @app.route('/config/category', methods=['POST', 'GET'])
  def category_get():
    if request.method == "GET": # Empty form
      return render_template('edit_category.html', nav=NavHelper(NavHelper.CONFIG))

    # Create new or update existing
    cid = request.form.get('category_id', None)
    log.debug('save category: %s', cid)
    if cid is None:
      category = Category()
    else:
      category = Category.get(Category.id == cid)

    category.name = request.form['category_name']
    category.save()
    return redirect(url_for('config'))

  @app.route('/config/category/<category_id>', methods=['GET'])
  def category_modify(category_id):
    category = Category.get(Category.id == category_id)
    return render_template('edit_category.html', category=category, nav=NavHelper(NavHelper.CONFIG))

  @app.route('/config/category/<category_id>/delete', methods=['GET'])
  def category_delete(category_id):
    log.debug('delete category: %s', category_id)
    category = Category.get(Category.id == category_id)
    category.delete_instance()
    return redirect(url_for('config'))
