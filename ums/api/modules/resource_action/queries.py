import logging
from ums.db import database
from ums.db.models.role_user_model import RoleUserModel
from ums.db.models.access_model import UserAccessModel
from ums.db.models.role_model import RolesModel
from ums.db.models.resource_action_model import ResourceActionModel
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from uuid import UUID
LOGGER = logging.getLogger(__package__)


def find_action_by_resource(resource_name: str):
    result = (
        database.session.query(
            ResourceActionModel.id.label("res_act_id"),
            ActionModel.name.label("action_name")
        )
        .outerjoin(
            ResourceModel,
            ResourceActionModel.resource_id == ResourceModel.id
        )
        .outerjoin(
            ActionModel,
            ResourceActionModel.action_id == ActionModel.id
        )
        .filter(ResourceModel.name == resource_name)
        .filter(ResourceActionModel.is_active)
        .all()
    )
    print("result", result)
    if result:
        json_array = []
        for record in result:
            json_object = {}
            for field, value in record._asdict().items():
                if isinstance(value, (UUID)):
                    value = str(value)
                json_object[field] = value
            json_array.append(json_object)
        LOGGER.debug(f"json_array: {json_array}")
        return json_array
    return None
