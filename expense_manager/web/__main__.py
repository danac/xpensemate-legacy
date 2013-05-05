#!/usr/bin/python

from bottle import route, run, jinja2_template as template, jinja2_view as view, static_file
import bottle

PREFIX=""

def getSampleBalance():
    exp1 = Expense(2, 2013, 4, 20, "Dana", 18, "Trucs...")
    exp2 = Expense(2, 2013, 4, 21, "Mik", 32, "Trucs...")
    exp3 = Expense(2, 2013, 4, 18, "Alizée", 10, "Trucs...")

@route("/")
@view("balance_list.html")
def index():
    return dict(prefix=PREFIX, return_link="www.google.com")

@route("/open_balances")
@view("balance.html")
def index():
    return dict(prefix=PREFIX, return_link=PREFIX + "/")

@route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root='/home/dchriste/devel/donjon/expense_manager/expense_manager/web/static')

if __name__ == "__main__":
    print(bottle.TEMPLATE_PATH)
    run(host='localhost', port=8080, reloader=True)
