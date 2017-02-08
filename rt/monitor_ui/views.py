from flask import Blueprint, request, g, redirect, url_for, abort, \
     render_template, flash, current_app  #,session

from rt.db import engine
from rt.monitor import db
from rt.monitor_ui.base import Monitor

bp = Blueprint(
    'monitor_ui',
    __name__,
    url_prefix='/monitor',
    static_folder='static/',
    template_folder='templates/')


@bp.route('/')
def starting_page():
    # return "Well..."
    return redirect(url_for('.show_monitors'))


@bp.route('/monitors')
def show_monitors():
    with engine.session_scope() as session:
        monitors = db.Monitor.get_monitors_for_ui(session)
    return render_template('monitor_ui/show_monitors.html', monitors=monitors)


@bp.route('/add', methods=['POST'])
def add_monitor():
    new_monitor = Monitor(
        display_name=request.form['name'],
        url=request.form['url'],
        mechanism_name=request.form['mechanism'],
        interval=request.form['interval'],
        enabled=request.form['enabled'],
    )
    with engine.session_scope() as session:
        db.Monitor.add_monitor(session, new_monitor)
    flash('New entry was successfully posted')
    return redirect(url_for(show_monitors))


@bp.route("/monitor/<name>")
def show_monitor_entries(name):
    with engine.session_scope() as session:
        monitor = session.query(db.Monitor).filter(
            db.Monitor.display_name == name
        ).first()
        if monitor:
            id = monitor.id
            entries = session.query(db.MonitorValue).filter(
                db.MonitorValue.monitor_id == id
            )
            return render_template('monitor_ui/show_monitor_entries.html', entries=entries)
    return abort(404)
