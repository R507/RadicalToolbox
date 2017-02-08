"""File writer that writes timestamp to the specific file every n seconds"""

import datetime
import logging
import os
import time

# TODO: path handler class?
PATH_TO_FILE = os.path.normpath(r"rt_omfw.log")

DELAY = 1


logger = logging.getLogger(__name__)


class FileHandler(object):
    """Handler for basic file operations"""
    def __init__(self, file):
        self._file = file

    def clean_file(self):
        """Just clean the file"""
        with open(self._file, "w"):
            pass

    def write_line(self, line):
        """Write line to a file"""
        with open(self._file, "a") as file:
            line = str(line)
            file.write(line)
            file.write("\n")


class EveryMinuteWriter(FileHandler):
    """Writes timestamp to file every minute"""
    INTERVAL = 30  # seconds

    def __init__(self, file):
        super().__init__(file)
        self._last_write_time = None  # type: datetime.datetime
        self._current_time = None  # type: datetime.datetime
        self._start()

    def tick(self):
        """Update timer"""
        self._current_time = datetime.datetime.now()

    @property
    def timedelta(self):
        """Get timedelta"""
        delta = self._current_time - self._last_write_time
        return delta

    def _write_current_time(self):
        """Write current time to file, preserve time of write"""
        self.write_line(self._current_time)
        self._last_write_time = self._current_time

    def _start(self):
        """Do initial actions, should be completed before process"""
        self.tick()
        self.clean_file()
        self._write_current_time()

    def process(self):
        self.tick()
        if self.timedelta > datetime.timedelta(seconds=self.INTERVAL):
            logger.info("Writing timestamp to file %s", self._current_time)
            self._write_current_time()


def main():
    writer = EveryMinuteWriter(PATH_TO_FILE)
    while True:
        logger.debug("Tick")
        writer.process()
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
