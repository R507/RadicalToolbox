import datetime


# TODO: get rid of this?
def get_current_datetime():
    value = datetime.datetime.now()
    return value


def deploy_iterable(iterable, session):
    for item in iterable:
        session.add(item)

