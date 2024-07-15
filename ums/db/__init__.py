import logging
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from ums.settings import settings

# ? Ref: https://github.com/ericmbernier/ericbernier-blog-posts/tree/master/flask_rest_api/football_api  # noqa
# ? Ref: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#query-the-data  # noqa

meta = sa.MetaData()

LOGGER = logging.getLogger(__package__)


class SqlalchemyBase(DeclarativeBase):
    """Base for all models."""

    metadata = meta


database = SQLAlchemy(model_class=SqlalchemyBase)


def init_database(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.db_url)
    LOGGER.info("Attempting DB setup.")
    database.init_app(app=app)
    LOGGER.info("Database connection established")
    if settings.auto_generate_tables:
        LOGGER.debug("Creating tables.")
        database.create_all()
        LOGGER.info(
            f"Created app tables - {list(SqlalchemyBase.metadata.tables.keys())}",
        )
