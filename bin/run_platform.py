import logging

import rt.config as config
import rt.logger as logger_module
from rt.platform.main import mainloop

logger = logging.getLogger(__name__)


def main():
    try:
        logger_module.setup_logging()
        logger.info("Starting execution")
        config.init()
        mainloop()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Exception caught', exc_info=True)
        raise


if __name__ == '__main__':
    main()
