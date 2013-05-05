#!/usr/bin/python

import os.path, inspect
import bottle

web_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

URL_PREFIX = "expense_manager2"
TEMPLATE_DIR = os.path.join(web_module_dir, "templates")
STATIC_DIR = os.path.join(web_module_dir, "static")

