#!/usr/bin/python

import os.path, inspect

web_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class WebParams:
    template_dir = os.path.join(web_module_dir, "templates")
    static_dir = os.path.join(web_module_dir, "static")
    exp_mgr = None
