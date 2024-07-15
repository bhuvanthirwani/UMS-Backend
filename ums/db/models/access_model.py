from uuid import uuid4

from sqlalchemy import (
    UUID,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    event,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.schema import CheckConstraint
from validator_collection import errors, validators

from ums.db.base import ModelBase
from ums.db.utils.password import hash_pswd_before_save


from .enums import UmsAppsEnum

USERNAME_MIN_LENGTH = 3


class UserAccessModel(ModelBase):
    """User model"""

    __admin__ = False
    __tablename__ = "user_credentials"

    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    name = Column(String(), nullable=False)
    username = Column(String(), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(), nullable=True, default="", server_default="")
    phone = Column(String(), nullable=False, unique=False)
    internal_user = Column(Boolean(), nullable=False, default=False)
    application = Column(UmsAppsEnum, nullable=False)
    last_login = Column(DateTime(), nullable=True)
    

    __table_args__ = (
        CheckConstraint(
            f"char_length(username) > {USERNAME_MIN_LENGTH}",
            name="user_username_min_length",
        ),
    )

    def __unicode__(self):
        return self.name

    @validates("username")
    def validate_username(self, key: str, value: str):
        if len(value) <= USERNAME_MIN_LENGTH:
            raise ValueError("user username should have minimum 3 characters")
        return value

    @validates("email")
    def validate_email(self, key: str, value: str):
        if not validators.email(value):
            raise errors.InvalidEmailError("Invalid email for user")
        return value

    def __repr__(self):
        return f"""
            name: {self.name}, username: {self.username}, email: {self.email},
            phone: {self.phone}, internal_user: {self.internal_user},
            application: {self.application}
        """


event.listen(UserAccessModel, "before_insert", hash_pswd_before_save)
event.listen(UserAccessModel, "before_update", hash_pswd_before_save)
