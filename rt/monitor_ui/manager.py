from flask import Flask, g
from werkzeug.utils import find_modules, import_string


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('rt.monitor_ui.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def create_app(config=None):
    app = Flask('monitor_ui')

    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='development key',  # TODO: check wtf is this affects
        USERNAME='admin',
        PASSWORD='default',
    ))
    app.config.update(config or {})
    # app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    register_blueprints(app)
    # register_cli(app)
    # register_teardowns(app)

    # app.debug = 1  # TODO: remove for prod

    return app



