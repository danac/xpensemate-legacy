def app(exp_mgr, prefix, referrer_url):
    from .config import WebParams
    WebParams.referrer_url = referrer_url
    WebParams.url_prefix = prefix
    WebParams.exp_mgr = exp_mgr
    from . import bottle_app
    return bottle_app.app
