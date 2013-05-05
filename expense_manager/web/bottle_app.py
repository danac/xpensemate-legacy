#!/usr/bin/python

import bottle
from .. import ExpenseManager
from .config import WebParams
from urllib.parse import urljoin
import datetime

app = bottle.Bottle()
bottle.TEMPLATE_PATH.insert(0, WebParams.template_dir)

prefix = WebParams.url_prefix
static_dir = WebParams.static_dir
exp_mgr = WebParams.exp_mgr

@app.route("/")
@bottle.jinja2_view('balance_list.html')
def open_balances():
    balances = exp_mgr.get_open_balances()
    return dict(prefix=prefix, return_link=urljoin(prefix, '..'), balances=balances, title="Bilans ouverts")

@app.route("/balance/<balID:int>")
@bottle.jinja2_view('balance.html')
def balance(balID):
    balance = exp_mgr.get_balance(id = balID)
    today = datetime.date.today().strftime('%Y-%m-%d')
    return dict(prefix=prefix, return_link=prefix + "/", balance = balance, today=today)

@app.route ("/dispatch", method='POST')
def dispatch():
    rep = ""
    for i in bottle.request.POST:
        rep += "{}: {}<br>".format(i, bottle.request.POST.get(i))
    return rep

@app.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=static_dir)

