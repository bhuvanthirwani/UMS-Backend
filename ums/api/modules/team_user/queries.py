import logging
from ums.db import database
from ums.db.models.role_user_model import RoleUserModel
from ums.db.models.access_model import UserAccessModel
from ums.db.models.role_model import RolesModel
from uuid import UUID
LOGGER = logging.getLogger(__package__)


def find_users_by_role(role_name: str):
    result = (
        database.session.query(
            RoleUserModel.id.label("role_user_id"),
            UserAccessModel.username.label("username")
        )
        .outerjoin(
            UserAccessModel,
            RoleUserModel.user_id == UserAccessModel.id
        )
        .outerjoin(
            RolesModel,
            RoleUserModel.role_id == RolesModel.id
        )
        .filter(RolesModel.name == role_name)
        .filter(RoleUserModel.is_active)
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
