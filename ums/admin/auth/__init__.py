from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import String, Column, UUID, event
from ums.db.utils.password import hash_pswd_before_save


class AdminModel(ModelBase):
    """Admin model"""

    __tablename__ = "auth_super_admins"
    __admin__ = False

    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    first_name = Column(String(100))
    last_name = Column(String(100))
    login = Column(String(80), nullable=False)
    password = Column(String(255), nullable=False)

    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.login

    def __repr__(self):
        return f"Admin: {self.first_name} {self.last_name}"


event.listen(AdminModel, "before_insert", hash_pswd_before_save)
event.listen(AdminModel, "before_update", hash_pswd_before_save)
