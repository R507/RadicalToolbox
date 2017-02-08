from rt import config
# from rt.monitor_ui import manager
from rt.platform_ui import manager
import rt.logger as logger_module


def main():
    logger_module.setup_logging()
    # # TODO: own logging config
    # monitor_ui.app.run(host=config.UI_HOST, port=config.UI_PORT)
    # # TODO: http://flask.pocoo.org/docs/0.12/deploying/#deployment
    app = manager.create_app()
    print(app.url_map)  # some debug info
    app.run(host=config.UI_HOST, port=config.UI_PORT)


if __name__ == '__main__':
    main()
