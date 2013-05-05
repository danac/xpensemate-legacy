#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle
from expense_manager.core import Expense, Balance
import expense_manager.web

if __name__ == "__main__":
    expense_manager.web.URL_PREFIX = "/test"
    instance = expense_manager.web.bottle_application()
    bottle.mount("/test", instance)
    bottle.run(host='localhost', port=8080, reloader=True)
