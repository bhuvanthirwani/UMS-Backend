import os
import logging
import functools
from flask import Flask
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from ums.settings import settings
from ums.logging import configure_logging
from ums.api.lifetime import register_startup_event


def flask_app() -> Flask:
    # TODO: Custom exception https://github.com/flask-restful/flask-restful/issues/280
    return Flask(
        __name__,
        static_folder=os.path.join(settings.base_path, "static"),
        root_path=settings.base_path,
    )


def app_setup(app: Flask):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            configure_logging(**{"log_level": settings.log_level, 'app': app})
            # Adds startup and shutdown events.
            app.secret_key = settings.session_secret
            app.config["MAX_CONTENT_LENGTH"] = settings.max_file_size_allowed
            CORS(app, resources={r"/api/*": {"origins": "*"}})
            with app.app_context():
                register_startup_event(app)

            # Add Sentry.
            if settings.sentry_dsn:
                sentry_sdk.init(
                    dsn=settings.sentry_dsn,
                    traces_sample_rate=settings.sentry_sample_rate,
                    environment=settings.environment,
                    integrations=[
                        FlaskIntegration(transaction_style="endpoint"),
                        LoggingIntegration(
                            level=logging.getLevelName(settings.log_level.value),
                            event_level=logging.ERROR,
                        ),
                        SqlalchemyIntegration(),
                    ],
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
