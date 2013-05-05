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
parent = urljoin(prefix, '..')
root = urljoin(prefix, '/')

@app.route("/")
@bottle.jinja2_view('balance_list.html')
def open_balances():
    balances = exp_mgr.get_open_balances()
    title = []
    title.append(dict(title="Bilans ouverts"))
    title.append(dict(title="Bilans fermés", link="closed"))
    persons = ', '.join(exp_mgr.get_persons())
    return dict(prefix=prefix, return_link=parent, balances=balances, title=title, editable = True, persons=persons)

@app.route("/closed")
@bottle.jinja2_view('balance_list.html')
def closed_balances():
    balances = exp_mgr.get_closed_balances()
    title = []
    title.append(dict(title="Bilans ouverts", link=parent))
    title.append(dict(title="Bilans fermés"))
    return dict(prefix=prefix, return_link=parent, balances=balances, title=title, editable = False)

@app.route("/balance/<balID:int>")
@bottle.jinja2_view('balance.html')
def balance(balID):
    balance = exp_mgr.get_balance(id = balID)
    open = True
    return_link = root
    if balance.year is not None:
        open = False
        return_link = urljoin(return_link, 'closed')
    today = datetime.date.today().strftime('%Y-%m-%d')
    return dict(prefix=prefix, return_link=return_link, balance = balance, today=today, editable=open)

@app.route ("/dispatch", method='POST')
def dispatch():
    action = bottle.request.forms.get("action")
    if action == "balance-close":
        exp_mgr.close_balance(bottle.request.forms.get('balance_id'))
        bottle.redirect(root)
    elif action == "balance-insert":
        exp_mgr.add_balance(bottle.request.forms.debtors) # Unicode fix
        bottle.redirect(root)
        rep += "EXPENSE-INSERT<br>"
    elif action == "expense-insert":
        rep += "EXPENSE-INSERT<br>"
    elif action == "expense-delete":
        rep += "EXPENSE-DELETE<br>"

    for i in bottle.request.POST:
        rep += "{}: {}<br>".format(i, bottle.request.POST.get(i))
    return rep

@app.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=static_dir)

