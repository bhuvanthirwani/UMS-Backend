from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import UUID, Column, ForeignKey
from ums.db.models.access_model import UserAccessModel
from ums.db.models.resource_action_model import ResourceActionModel


class UserResourceActionModel(ModelBase):
    __tablename__ = "user__resource_action"
    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    user_id = Column(UUID(), ForeignKey(UserAccessModel.id))
    res_act_id = Column(UUID(), ForeignKey(ResourceActionModel.id))

    __table_args__ = {'extend_existing': True}
