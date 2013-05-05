#!/usr/bin/python
# -*- coding: utf-8 -*-#

#boilerplate to allow running as script directly
if __name__ == "__main__" and __package__ is None:
    import sys, os
    # The following assumes the script is in the top level of the package
    # directory.  We use dirname() to help get the parent directory to add to
    # sys.path, so that we can import the current package.  This is necessary
    # since when invoked directly, the 'current' package is not automatically
    # imported.
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    import expense_manager
    __package__ = str("expense_manager")
    del sys, os
# now you can use relative imports here that will work regardless of how this
# python file was accessed (either through 'import', through 'python -m', or
# directly.

from .web import app
from . import ExpenseManager

prefix = ""
exp_mgr = ExpenseManager(db_file="test_database.db")
webapp = app(exp_mgr, prefix)
webapp.run(host='localhost', port=8080, reloader=True)
