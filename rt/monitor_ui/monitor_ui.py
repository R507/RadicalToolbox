import flask
from flask import request, abort

from rt.db import definitions
from rt.db import engine
from rt.path import Path


# TODO: REFACTOR THIS GARBAGE!!!


app = flask.Flask(
    __name__,
    # template_folder=str(Path('../rt/monitor_ui/templates')),
    template_folder=str(Path('templates')),  # TODO: fix it?
    static_folder=str(Path('static')),  # TODO: fix it?
)
app.config.from_object(__name__)

app.config.update(
    dict(
        SECRET_KEY='development key',  # TODO: check wtf is this affects
        USERNAME='admin',
        PASSWORD='default',
    )
)

app.debug = 1  # TODO: remove for prod


def url_for(function):
    return flask.url_for(function.__name__)


@app.route("/")
def starting_page():
    # return "Well..."
    return flask.redirect(url_for(show_monitors))


@app.route("/monitors")
def show_monitors():
    with engine.session_scope() as session:
        monitors = session.query(definitions.Monitor)
    return flask.render_template('show_monitors.html', monitors=monitors)


@app.route("/monitor/<name>")
def show_monitor_entries(name):
    with engine.session_scope() as session:
        monitor = session.query(definitions.Monitor).filter(
            definitions.Monitor.display_name == name
        ).first()
        if monitor:
            id = monitor.id
            entries = session.query(definitions.MonitorValue).filter(
                definitions.MonitorValue.monitor_id == id
            )
            return flask.render_template('show_monitor_entries.html',
                                         entries=entries)
    return abort(404)


@app.route('/add', methods=['POST'])
def add_monitor():
    new_monitor = definitions.Monitor(
        display_name=request.form['name'],
        url=request.form['url'],
        mechanism_name=request.form['mechanism'],
        interval=request.form['interval'],
        enabled=request.form['enabled'],
    )
    with engine.session_scope() as session:
        session.add(new_monitor)
    flask.flash('New entry was successfully posted')
    return flask.redirect(url_for(show_monitors))


@app.route("/redirect")
def redirect_page():
    # return flask.redirect(flask.url_for(show_monitors.__name__))
    return flask.redirect(url_for(show_monitors))


@app.route('/entries/<monitor_display_name>')
def show_monitor_data(monitor_display_name):
    # This should return collected monitor data
    return "Placeholder for {}".format(monitor_display_name)
