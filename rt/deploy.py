from rt.db import engine

import rt.platform.db as platform_db
import rt.monitor.db as monitor_db


def deploy_modules_entries(*modules, session):
    for module in modules:
        module.deploy_entries(session)  # TODO: make module a class?
        # and in the base class explicitly raise NotImplementedError
        # in deploy_entries


def deploy_db():
    engine.Base.metadata.create_all(engine.main_engine)
    with engine.session_scope() as session:
        deploy_modules_entries(
            platform_db,
            monitor_db,
            session=session,
        )
