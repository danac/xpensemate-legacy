#!/usr/bin/python

import bottle
from . import URL_PREFIX, STATIC_DIR, TEMPLATE_DIR

app = bottle.Bottle()
bottle.TEMPLATE_PATH.insert(0, TEMPLATE_DIR)

@app.route("/")
@bottle.jinja2_view('balance_list.html')
def balance_list():
    return dict(prefix=URL_PREFIX, return_link="")

@app.route("/balance/<balID:int>")
@bottle.jinja2_view('balance.html')
def balance(balID):
    return dict(prefix=URL_PREFIX, return_link=URL_PREFIX + "/", balID=balID)

@app.route ("/dispatch")
def dispatch():
    pass

@app.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=STATIC_DIR)
