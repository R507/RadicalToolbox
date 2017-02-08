import enum
from rt.base.objects import Structure


class ErrorCode(enum.IntEnum):
    """Universal error codes for scraping"""
    SUCCESS = 0
    NO_CONTENT = 1
    UNHANDLED_ERROR = 255


class Parameters(Structure):
    def __init__(
            self,
            scraper,
            url,
            monitor_id,
            interval

    ):
        self.scraper = scraper
        self.url = url
        self.monitor_id = monitor_id
        self.interval = interval
