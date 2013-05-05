
def app(exp_mgr, prefix):
    from .config import WebParams
    WebParams.url_prefix = prefix
    WebParams.exp_mgr = exp_mgr
    from . import bottle_app
    return bottle_app.app
