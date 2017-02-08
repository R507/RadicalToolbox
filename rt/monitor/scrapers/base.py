import datetime
import logging
import traceback

import requests

from rt.base.objects import Structure
from rt.monitor.base import ErrorCode

logger = logging.getLogger(__name__)


class Result(Structure):
    def __init__(
            self,
            value,
            error_code,
            timestamp=None,
    ):
        self.value = value
        self.error_code = error_code
        self.timestamp = timestamp or datetime.datetime.now()


class Scraper(object):
    """Somewhat primitive scraper, takes just the url and extracts
    result, putting in JSON structure"""

    @classmethod
    def _get_content(cls, url):
        logger.info("Retrieving content for url - {}".format(url))
        page = requests.get(url)
        content = page.content
        logger.info("Retrieved content for url - {}".format(url))
        return content

    @classmethod
    def _extract_value(cls, content):
        """Should be implemented in concrete scraper

        :returns: result formatted as JSON structure dict"""
        raise NotImplementedError

    @classmethod
    def get_result(cls, url):
        try:
            logger.debug("Getting value for url - {}".format(url))
            content = cls._get_content(url)
            logger.debug("Retrieved content - {}".format(content))
            # value should be json serializable struct
            value = cls._extract_value(content)
            result = Result(value=value, error_code=ErrorCode.SUCCESS)
            logger.debug("Retrieved result - {}".format(result))
            return result
        except Exception as e:  # TODO: yes, this is sooo broad, but is there a better way?
            result = Result(
                value={
                    'error': True,
                    'exception': repr(e),
                    'traceback': traceback.format_tb(e.__traceback__),
                },
                error_code=ErrorCode.UNHANDLED_ERROR
            )
            logging.exception('Unhandled error - {}'.format(result))
            return result


