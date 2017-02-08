"""Configuration module

Provides functionality to load configuration file and provide
settings from it to peers"""
import logging

from rt.path import Path

logger = logging.getLogger(__name__)


# TODO: take configuration from .json file
DB_PATH = Path("main.db")
DB_TYPE = 'sqlite'
UI_HOST = '127.0.0.1'
UI_PORT = 5001

SLEEP_TIME = 1


def init():
    """Initialize the configuration"""
    # well, nothing to init at the moment
    logger.info("Configuration initialized")
