
# class Helpers(object):

class NavLocation(object):
  HOME = 1
  CONFIG = 2
  _status_map = {HOME: 'home', CONFIG: 'config'}

class NavHelper(object):
  HOME = 1
  def __init__(self, location):
    self.location = location

  def nav_home(self):
    return self.location == NavLocation.HOME

  def nav_config(self):
    return self.location == NavLocation.CONFIG