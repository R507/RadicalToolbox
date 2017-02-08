from flask_nav.elements import Navbar, View
from flask_nav import Nav


topbar = Navbar('RT',
    View('Home', 'platform_ui.starting_page'),
    View('Monitor', 'monitor_ui.show_monitors'),
)


def init_app_navbar(app):
    nav = Nav()
    nav.register_element('top', topbar)
    nav.init_app(app)
