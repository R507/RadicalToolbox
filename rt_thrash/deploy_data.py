"""Deploy some data into DB for test purposes"""
from rt.monitor import db
from rt.db import engine


def deploy_some_data():
    ct_monitor = db.Monitor(
        display_name='ct_palit_1050ti',
        url=
        'https://www.citilink.ru/catalog/computers_and_notebooks/parts/videocards/405775/',
        mechanism_name='Citilink.ru',
        interval=240,
        enabled=True,
    )
    ct_monitor_failure = db.Monitor(
        display_name='ct_forever_fail',
        url=
        'https://www.cccitilink.ru/catalog/computers_and_notebooks/parts/videocards/405775/',
        mechanism_name='Citilink.ru',
        interval=240,
        enabled=True,
    )
    with engine.session_scope() as session:
        session.add(ct_monitor)
        session.add(ct_monitor_failure)
