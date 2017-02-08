import logging

from sqlalchemy import Column, Integer, String, Boolean

from rt.db.engine import Base
from rt.db.helper import deploy_iterable
from rt.monitor import manager as monitor_manager
from rt.platform.base import ManagerParameters

logger = logging.getLogger(__name__)


# TODO: This is awful that platform contains dependencies on EVERY module
# try to do something with it
MODULES_NAME_MAP = {
    # name: module manager
    "monitor": monitor_manager,
}


class Manager(Base):
    __tablename__ = 'manager'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    manager_name = Column(String(100), unique=True, nullable=False)
    enabled = Column(Boolean, nullable=False)

    @classmethod
    def get_parameters_for_active(cls, session):
        managers = session.query(cls).filter(cls.enabled).all()
        parameters = [
            ManagerParameters(manager=MODULES_NAME_MAP[manager.manager_name])
            for manager in managers
        ]
        return parameters


def manager_entries():
    """Manager entries based on mapping"""
    for key in MODULES_NAME_MAP.keys():
        module_entry = Manager(manager_name=key, enabled=True)
        yield module_entry


def deploy_entries(session):
    """Deploy initial platform entries on creation"""
    deploy_iterable(manager_entries(), session)
