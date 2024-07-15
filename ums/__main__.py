import os
import shutil

from flask import Flask
from ums.api import bootstrap
from ums.api.application import flask_app
from ums.settings import settings, Environment


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multi process directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behavior.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    os.makedirs(settings.prometheus_dir, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


def main() -> Flask:
    """Entrypoint of app, setup flask application."""
    set_multiproc_dir()
    return bootstrap(app=flask_app())


if __name__ == "__main__":
    app = main()
    
    app.run(
        host=settings.host,
        port=settings.port,
        debug=bool(settings.environment == Environment.DEV),
    )
