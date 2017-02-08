"""Main Platform manager

Controls other managers"""
import logging


from rt.db import engine
from rt.platform import db

logger = logging.getLogger(__name__)


def execute():
    """Execute all active managers"""
    with engine.session_scope() as session:
        managers_parameters = db.Manager.get_parameters_for_active(session)
    for manager_parameters in managers_parameters:
        logger.info('Executing manager {!r}'.format(manager_parameters))
        manager_parameters.manager.execute()
        logger.info('Manager execution finished')
