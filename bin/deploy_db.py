import os

from rt import config
from rt import deploy
from rt_thrash import deploy_data  # TODO: remove it at some point


def main():
    try:
        os.remove(str(config.DB_PATH))  # TODO: probably improve this line
    except FileNotFoundError:
        pass
    deploy.deploy_db()
    deploy_data.deploy_some_data()


if __name__ == '__main__':
    main()
