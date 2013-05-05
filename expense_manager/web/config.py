#!/usr/bin/python

import os.path, inspect

web_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

URL_PREFIX = ""#"expense_manager2"
TEMPLATE_DIR = os.path.join(web_module_dir, "templates")
STATIC_DIR = os.path.join(web_module_dir, "static")
SERVER_PORT = 8080
