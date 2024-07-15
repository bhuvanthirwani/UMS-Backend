from uuid import uuid4
from sqlalchemy import (
    UUID,
    Column,
    String,
)

from ums.db.base import ModelBase

USERNAME_MIN_LENGTH = 3


class RolesModel(ModelBase):
    __tablename__ = "roles"

    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    name = Column(String(), unique=True, nullable=False)

    # Define a one-to-many relationship with User
    # users = relationship("UserAccessModel", back_populates="roles")

    # Define a many-to-many relationship with Role
    def __repr__(self) -> str:
        return f"""
            name: {self.id} \n
            username: {self.name} \n
        """
