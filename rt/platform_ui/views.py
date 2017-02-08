from flask import Blueprint, request, g, redirect, url_for, abort, \
     render_template, flash, current_app  #,session

from rt.db import engine
from rt.monitor import db
from rt.monitor_ui.base import Monitor

bp = Blueprint(
    'platform_ui',
    __name__,
    static_folder='static/',
    static_url_path='/static/',
    template_folder='templates/')


@bp.route('/')
def starting_page():
    # return "Well..."
    return render_template('platform_ui/index.html')
