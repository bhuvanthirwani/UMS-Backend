from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from ums.db.models.role_model import RolesModel
from ums.db.models.access_model import UserAccessModel


class RoleUserModel(ModelBase):
    __tablename__ = "role_user"
    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    role_id = Column(UUID(), ForeignKey(RolesModel.id))
    user_id = Column(UUID(), ForeignKey(UserAccessModel.id))
