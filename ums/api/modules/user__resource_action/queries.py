import logging
from ums.db import database
from ums.db.models.access_model import UserAccessModel
from ums.db.models.user_res_act_model import UserResourceActionModel
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from ums.db.models.resource_action_model import ResourceActionModel
from uuid import UUID
LOGGER = logging.getLogger(__package__)


def find_resource_action_by_user(username: str):
    result = (
        database.session.query(
            UserResourceActionModel.id.label("user_res_act_id"),
            ResourceModel.name.label("resource_name"),
            ActionModel.name.label("action_name")
        )
        .outerjoin(
            ResourceActionModel,
            ResourceActionModel.id == UserResourceActionModel.res_act_id

        )
        .outerjoin(
            ResourceModel,
            ResourceActionModel.resource_id == ResourceModel.id
        )
        .outerjoin(
            ActionModel,
            ResourceActionModel.action_id == ActionModel.id
        )
        .outerjoin(
            UserAccessModel,
            UserResourceActionModel.user_id == UserAccessModel.id
        )
        .filter(UserAccessModel.username == username)
        .filter(UserResourceActionModel.is_active)
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
