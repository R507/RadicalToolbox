# TODO: I probably need an interface/facade for this file, or do I?
import json
import logging

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, JSON
from sqlalchemy import TypeDecorator
from sqlalchemy import desc
from sqlalchemy.ext import mutable
from sqlalchemy.orm import relationship

from rt import config
from rt.monitor.base import Parameters
from rt.db.engine import Base
from rt.db.helper import deploy_iterable
from rt.monitor.scrapers.citilink import Scraper as Citilink  # TODO: do something with this import
from rt.monitor_ui.base import Monitor as UIMonitor

logger = logging.getLogger(__name__)

SCRAPER_DISPLAY_NAME_MAP = {
    # name: scraper
    # TODO: name should be lowercase and match base http address for auto
    # scraper chooser
    "Citilink.ru": Citilink,  # TODO: rename to lowercase
}


# TODO: move it to monitor_db subproject? since it depens on everything that
# uses it


class JsonEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    # def copy(self, **kw):
    #     # TODO: ahem..., wtf is this method?
    #     return JsonEncodedDict()

mutable.MutableDict.associate_with(JsonEncodedDict)


class MonitorValue(Base):
    __tablename__ = "monitor_value"
    id = Column(Integer, primary_key=True)
    monitor_id = Column(Integer, ForeignKey('monitor.id'), nullable=False)

    # TODO: better move DB_TYPE value as define somewhere
    # to not have multiple references to one place
    if config.DB_TYPE == 'sqlite':
        value = Column(JsonEncodedDict, nullable=False)
    else:
        value = Column(JSON, nullable=False)

    # TODO: checkout the Float(asdecimal=True)
    # sqlalchemy docs tell that decimal is slow,
    # but cdecimal in 3.3 and later is better, check it out
    datetime = Column(DateTime, nullable=False)
    error_code = Column(Integer, nullable=False)

    @classmethod
    def save_value(cls, entry, session):
        logger.info('Saving entry, {!r}'.format(entry))
        entry = cls(
            monitor_id=entry.monitor_id,
            value=entry.value,
            datetime=entry.timestamp,
            error_code=entry.error_code,
        )
        session.add(entry)

    @classmethod
    def get_entry_last_timestamp(cls, monitor_id, session):
        # TODO: separate interval for failed entries?
        entry = session.query(cls).filter(
            cls.monitor_id == monitor_id).order_by(
            desc(cls.datetime)).limit(1).all()
        if entry:
            return entry[0].datetime
        return None


class Monitor(Base):
    __tablename__ = 'monitor'
    id = Column(Integer, primary_key=True)
    display_name = Column(String(200), unique=True, nullable=False)
    url = Column(String(500), nullable=False)
    mechanism_name = Column(
        String(100), ForeignKey('scraper.mechanism_name'), nullable=False)
    interval = Column(Integer, nullable=False)  # seconds? minutes?
    enabled = Column(Boolean, nullable=False)  # TODO: create one-to-one table instead? or not since it's not optional?
    monitor_value = relationship(MonitorValue)

    @classmethod
    def get_active_monitors_parameters(cls, session):
        monitors = session.query(cls).filter(cls.enabled).all()
        params = [
            Parameters(
                scraper=SCRAPER_DISPLAY_NAME_MAP[monitor.mechanism_name],
                url=monitor.url,
                monitor_id=monitor.id,
                interval=monitor.interval,
            )
            for monitor in monitors]
        return params

    @classmethod
    def get_monitors_for_ui(cls, session):
        """This method returns monitors list for monitor UI"""
        # TODO: this method specific to only one of the subprojects
        # how good it is to keep it here?
        monitors = session.query(cls)
        monitors_for_ui = [
            UIMonitor(
                url=monitor.url,
                display_name=monitor.display_name,
                mechanism_name=monitor.mechanism_name,
                interval=monitor.interval,
                enabled=monitor.enabled,
            )
            for monitor in monitors
        ]
        return monitors_for_ui

    @classmethod
    def add_monitor(cls, session, monitor_entry):
        # TODO: this should check validity of input, including mechanism name
        # error from here should be handled above...
        entry = cls(
            display_name=monitor_entry.display_name,
            url=monitor_entry.url,
            mechanism_name=monitor_entry.mechanism_name,
            interval=monitor_entry.interval,
            enabled=monitor_entry.enabled,
        )
        session.add(entry)


class Scraper(Base):
    __tablename__ = 'scraper'
    id = Column(Integer, primary_key=True)
    mechanism_name = Column(String(200), nullable=False)
    monitor = relationship(Monitor)


def scraper_entries():
    """Scraper entries based on mapping"""
    for key in SCRAPER_DISPLAY_NAME_MAP.keys():
        scraper_entry = Scraper(mechanism_name=key)
        yield scraper_entry


def deploy_entries(session):
    """Deploy initial platform entries on creation"""
    deploy_iterable(scraper_entries(), session)


if __name__ == '__main__':
    from pprint import pprint
    pprint(dir(JsonEncodedDict))
