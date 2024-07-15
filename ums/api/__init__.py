import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from ums.api.application import app_setup
from ums.api.routes import register_routes
from ums.settings import Environment, settings


def bootstrap(app: Flask) -> Flask:
    register_routes(app)
    logging.info("Route configuration successful.")

    @app_setup(app)
    def wrapper():
        if settings.environment != Environment.DEV:
            app.wsgi_app = ProxyFix(
                app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
            )
        return app

    return wrapper()
