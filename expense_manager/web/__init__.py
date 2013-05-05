from .config import URL_PREFIX, TEMPLATE_DIR, STATIC_DIR

def bottle_application():
    from . import bottle_app
    return bottle_app.app
