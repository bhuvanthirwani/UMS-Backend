import logging

from flask import Flask
from ums.api.monitoring import prometheus
from ums.db import init_database
from ums.settings import settings
from ums.admin.setup import setup_admin
from ums.api.security import setup_authorization

LOGGER = logging.getLogger(__package__)


def setup_prometheus(app: Flask) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    # ? Documentation - https://pypi.org/project/prometheus-flask-exporter/
    prometheus.init_app(app)


def register_startup_event(app: Flask) -> None:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses flaskAPI app to store data
    in the state, such as db_engine.

    :param app: the flaskAPI application.
    :return: function that actually performs actions.
    """
    setup_authorization(app=app)
    setup_prometheus(app)
    init_database(app)
    if settings.admin_enabled:
        setup_admin(app=app)


async def register_shutdown_event(app) -> None:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: flaskAPI application.
    :return: function that actually performs actions.
    """
    await app.config["db_engine"].dispose()
    LOGGER.info("Closing server...")
