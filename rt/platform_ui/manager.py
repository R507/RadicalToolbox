from flask import Flask, g
from werkzeug.utils import find_modules, import_string

import logging

from rt.platform_ui.navbar import init_app_navbar

LOGGER = logging.getLogger(__name__)


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('rt', recursive=True):
        if 'views' not in name:
            continue
        try:
            mod = import_string(name)
        except Exception:
            LOGGER.debug('Error loading module %s, ignoring...', name)
            continue
        if hasattr(mod, 'bp'):
            LOGGER.info('Registering module %s', name)
            app.register_blueprint(mod.bp)
        else:
            LOGGER.debug('Ignoring module %s', name)
    return None


def create_app(config=None):
    app = Flask(
        'platform_ui',
        static_url_path='/static_app/'  # without it'll conflict with platform_ui static folder
        # prolly should investigate simpler solution, since it kinda messy
    )

    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='development key',  # TODO: check wtf is this affects
        USERNAME='admin',
        PASSWORD='default',
    ))
    app.config.update(config or {})
    # app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    # app.register_blueprint(monitor_ui_bp, url_prefix='/monitor')
    register_blueprints(app)
    init_app_navbar(app)
    # register_cli(app)
    # register_teardowns(app)

    # app.debug = 1  # TODO: remove for prod

    return app

