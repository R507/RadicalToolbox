import time

from rt.platform import manager
from rt import config


def mainloop():
    while True:
        manager.execute()
        time.sleep(config.SLEEP_TIME)


if __name__ == '__main__':
    mainloop()
