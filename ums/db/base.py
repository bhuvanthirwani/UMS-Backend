import datetime

from sqlalchemy import Column, func, text
from sqlalchemy.types import Boolean, DateTime
from ums.db import database, SqlalchemyBase


class Base(SqlalchemyBase, database.Model):
    __abstract__ = True


class ModelBase(Base):
    """
    Model Base class with created_at and updated_at functionality.
    - To be able to use this across all table in the database.
    """

    __abstract__ = True

    created_at = Column(
        "created_at",
        DateTime,
        server_default=func.now(),
        default=datetime.datetime.now,
        nullable=False,
        doc="Entry created at",
        comment="row created at",
    )

    updated_at = Column(
        "updated_at",
        DateTime,
        server_default=func.now(),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
        doc="Entry last updated",
        comment="row last updated",
    )

    is_active = Column(
        "is_active",
        Boolean,
        server_default=text("true"),
        default=True,
        nullable=False,
        doc="soft deleted?",
        comment="soft deleted?",
    )
