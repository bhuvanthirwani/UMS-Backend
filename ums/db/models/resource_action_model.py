from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import UUID, Column, ForeignKey
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from sqlalchemy.orm.exc import NoResultFound


class ResourceActionModel(ModelBase):
    __tablename__ = "resource_action"
    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    resource_id = Column(UUID(), ForeignKey(ResourceModel.id))
    action_id = Column(UUID(), ForeignKey(ActionModel.id))

    def find_by_resource_action_id_pair(self, res_id: str, act_id: str):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query: dict = {}
            query["is_active"] = True
            query["resource_id"] = res_id
            query["action_id"] = act_id
            if len(query) > 0:
                entry: ResourceActionModel = self.query.filter_by(**query).one_or_none()
            else:
                entry: ResourceActionModel = self.query.one_or_none()

            # LOGGER.debug(f"status : {entry.id}")
            if entry:
                return str(entry.id)

            # LOGGER.debug(f"status_res : {type(res)}")
        except NoResultFound:
            return None
