"""Database table handler

Goes though DB table finds which items should be run"""
import datetime
import logging

from rt.db import engine
from rt.monitor import db
from rt.base.objects import Structure

logger = logging.getLogger(__name__)


class MonitorValueEntry(Structure):
    def __init__(
            self,
            monitor_id,
            value,
            timestamp,
            error_code

    ):
        self.monitor_id = monitor_id
        self.value = value
        self.timestamp = timestamp
        self.error_code = error_code


def get_monitors_to_execute(session):
    logger.debug("Getting list of monitor to execute")
    monitor_to_execute = []
    for monitor in db.Monitor.get_active_monitors_parameters(session):
        latest_entry_timestamp = db.MonitorValue.get_entry_last_timestamp(
            monitor_id=monitor.monitor_id,
            session=session)
        if not latest_entry_timestamp or datetime.timedelta(
                seconds=monitor.interval) < (
                    datetime.datetime.now() - latest_entry_timestamp):
            monitor_to_execute.append(monitor)
    return monitor_to_execute


def execute():
    logger.info("Executing Monitor Manager")  # TODO: make decorator for logs
    with engine.session_scope() as session:
        monitors_to_execute = get_monitors_to_execute(session)
    for parameters in monitors_to_execute:
        result = parameters.scraper.get_result(parameters.url)
        value_entry = MonitorValueEntry(
            monitor_id=parameters.monitor_id,
            value=result.value,
            timestamp=result.timestamp,
            error_code=result.error_code,
        )
        with engine.session_scope() as session:
            db.MonitorValue.save_value(value_entry, session)
    logger.info("Monitor Manager finished")
