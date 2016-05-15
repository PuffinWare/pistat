#!/usr/bin/env python
"""
Copyright (c) 2016 Puffin Software, All rights reserved.
"""

from gevent.monkey import patch_all; patch_all()
import sys
import os
import logging
from com.puffinware.pistat.routes import setup_routes
from logging.handlers import RotatingFileHandler
from flask import Flask
from argparse import ArgumentParser
from gevent.wsgi import WSGIServer
import json

DEFAULT_CONFIG_FILE = "config/config.json"

log = logging.getLogger(__name__)

def main(argv=None):
  parser = ArgumentParser(description="pistat.py [options]")
  parser.add_argument("-c", "--config", dest="config", default=DEFAULT_CONFIG_FILE, action="store", help="App config file")
  parser.add_argument("-d", "--debug", dest="debug", default=False, action="store_true", help="Run app in debug mode")
  parser.add_argument("-s", "--console", dest="console", default=False, action="store_true", help="Log to console")
  parser.add_argument("-p", "--port", dest="port", default=5555, type=int, action="store", help="Port number to run on")
  options = parser.parse_args()

  if not os.path.exists(options.config):
    print 'Supplied config file \'%s\' does not exist' % options.config
    sys.exit(1)

  webapp = Flask(__name__)
  webapp.config.update(json.load(open(options.config)))

  root_log = logging.getLogger()
  formatter = logging.Formatter("%(asctime)s %(levelname)-5s %(name)s(:%(lineno)d) %(message)s", '%Y.%m.%d-%H:%M:%S')
  if options.debug:
    root_log.setLevel(logging.DEBUG)
  else:
    root_log.setLevel(logging.INFO)

  if options.console:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_log.addHandler(console_handler)

  file_handler = RotatingFileHandler(webapp.config['log_file'], maxBytes=10240000, backupCount=5)
  file_handler.setFormatter(formatter)
  root_log.addHandler(file_handler)

  logging.getLogger('requests.packages.urllib3').setLevel(logging.WARNING)

  setup_routes(webapp)

  log.info("Starting pistat on %s | config file: %s | debug: %s", options.port, options.config, options.debug)
  if options.debug:
    webapp.run(host='0.0.0.0', port=options.port, debug=True)
  else:
    http_server = WSGIServer(('', options.port), webapp, log=None)
    http_server.serve_forever()

if __name__ == "__main__":
  main()