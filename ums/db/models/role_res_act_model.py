from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import UUID, Column, ForeignKey
from ums.db.models.resource_action_model import ResourceActionModel
from ums.db.models.role_model import RolesModel


class RoleResourceActionModel(ModelBase):
    __tablename__ = "role__resource_action"
    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    role_id = Column(UUID(), ForeignKey(RolesModel.id))
    res_act_id = Column(UUID(), ForeignKey(ResourceActionModel.id))

    __table_args__ = {'extend_existing': True}
