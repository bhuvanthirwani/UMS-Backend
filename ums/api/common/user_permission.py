from ums.db.models.access_model import UserAccessModel
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from ums.db.models.resource_action_model import ResourceActionModel
from ums.db.models.role_user_model import RoleUserModel
from ums.db.models.user_res_act_model import UserResourceActionModel
from ums.db.models.role_res_act_model import RoleResourceActionModel
from ums.db.models.role_model import RolesModel
from ums.db import database
from sqlalchemy import func, and_
import logging
LOGGER = logging.getLogger(__package__)


def user_base_permission(user_id: str) -> dict[str, set[str]]:
    print("here3333333333")
    result: dict[str, set[str]] = {}
    records = (
        database.session.query(
            ResourceModel.name.label("resource"),
            func.ARRAY_REMOVE(
                func.ARRAY_AGG(ActionModel.name), None
            ).label("action"),
        )
        .select_from(UserResourceActionModel)
        .outerjoin(
            UserAccessModel,
            UserResourceActionModel.user_id == UserAccessModel.id
        )
        .outerjoin(
            ResourceActionModel,
            UserResourceActionModel.res_act_id == ResourceActionModel.id
        ).outerjoin(
            ResourceModel,
            ResourceActionModel.resource_id == ResourceModel.id
        ).outerjoin(
            ActionModel,
            ResourceActionModel.action_id == ActionModel.id
        )
        .filter(UserAccessModel.id == user_id)
        .filter(UserResourceActionModel.is_active)
        .having(func.count(ResourceModel.id) > 0)
        .group_by(
            ResourceModel.name.label("resource"),
        )
    )
    LOGGER.debug(f"user query: {records}")
    records = records.all()
    LOGGER.debug(f"user records: {records}")
    if records:
        for record in records:
            result[record[0]] = set(record[1])
    LOGGER.debug(f"result: {result}")
    return result


def role_base_permission(role_id: list[str]) -> dict[str, set[str]]:
    print("here*******************")
    result: dict[str, set[str]] = {}
    records = (
        database.session.query(
            ResourceModel.name.label("resource"),
            func.ARRAY_REMOVE(
                func.ARRAY_AGG(ActionModel.name), None
            ).label("action"),
        )
        .select_from(RoleResourceActionModel)
        .outerjoin(
            RolesModel,
            RolesModel.id == RoleResourceActionModel.role_id
        ).outerjoin(
            ResourceActionModel,
            RoleResourceActionModel.res_act_id == ResourceActionModel.id
        ).outerjoin(
            ResourceModel,
            ResourceActionModel.resource_id == ResourceModel.id
        ).outerjoin(
            ActionModel,
            ResourceActionModel.action_id == ActionModel.id
        ).filter(RoleResourceActionModel.is_active)
        .filter(RolesModel.id == role_id)
        .group_by(
            ResourceModel.name.label("resource"),
        )
    )
    LOGGER.debug(f"user query: {records}")
    records = records.all()
    LOGGER.debug(f"role records: {records}")
    if records:
        for record in records:
            result[record[0]] = set(record[1])
    # LOGGER.debug(f"result: {result}")
    return result


def find_roles_by_user(user_id: str) -> list[str]:
    print(f"here22222222222: {user_id}")
    # result = (
    #     database.session.query(
    #         func.ARRAY_REMOVE(
    #             func.ARRAY_AGG(RoleUserModel.role_id), None
    #         ).label("role_id"),
    #     )
    #     .filter(and_(RoleUserModel.user_id == user_id, RoleUserModel.is_active))
    #     .all()
    # )

    # LOGGER.debug(f"here22222222222: result: {result}")
    # return result[0][0] if result[0][0] is not None else []
    role_ids = database.session.query(RoleUserModel.role_id).filter(RoleUserModel.user_id == user_id).all()
    # .filter(RoleUserModel.user_id == user_id)
    # and_(RoleUserModel.user_id == user_id, RoleUserModel.is_active)
    # .filter(RoleUserModel.is_active == True).all()

    print(f"here22222222222: result: {role_ids}")
    return [str(role.role_id) for role in role_ids]

def find_user_roles_name(user_id: str) -> list[str]:
    return [find_role_name_by_role_id(role_id) for role_id in find_roles_by_user(user_id)]

def find_role_name_by_role_id(role_id: str) -> list[str]:
    
    result = (
        database.session.query(
            RolesModel.name.label("role_name"),
        )
        .filter(and_(RolesModel.id == role_id, RolesModel.is_active))
        .all()
    )

    LOGGER.debug(f"result: {result}")
    return result[0][0] if result[0][0] is not None else []


def build_permission(user_id: str) -> dict[str, list[str]]:
    print("here1111111111111")
    user_permission: dict[str, set[str]] = user_base_permission(user_id=user_id)
    print("here1.555555555555")
    role_ids: list[str] = find_roles_by_user(user_id=user_id)
    for role_id in role_ids:
        role_permission: dict[str, set[str]] = role_base_permission(role_id=role_id)
        LOGGER.debug(f"user_permission: {user_permission}")
        LOGGER.debug(f"role_permission: {role_permission}")
        if role_permission:
            for perm in role_permission:
                if perm in user_permission:
                    user_permission[perm] = user_permission[perm].union(role_permission[perm])
                else:
                    user_permission[perm] = role_permission[perm]

    for perm in user_permission:
        user_permission[perm] = list(user_permission[perm])
    
    LOGGER.debug(f"final_user_permission: {user_permission}")
    return user_permission


def user_resource_action_permission(user_id: str):
    print("here")
    result = (
        database.session.query(
            UserResourceActionModel.res_act_id.label("resource_action_id"),
            ResourceModel.name.label("resource"),
            ActionModel.name.label("action"),
        )
        .outerjoin(
            UserAccessModel,
            UserResourceActionModel.user_id == UserAccessModel.id
        )
        .outerjoin(
            ResourceActionModel,
            UserResourceActionModel.res_act_id == ResourceActionModel.id
        ).outerjoin(
            ResourceModel,
            ResourceActionModel.resource_id == ResourceModel.id
        ).outerjoin(
            ActionModel,
            ResourceActionModel.action_id == ActionModel.id
        )
        .filter(UserAccessModel.id == user_id)
        .filter(UserResourceActionModel.is_active)
        .all()
    )

    if result:
        json_array = []
        for record in result:
            json_object = {}
            for field, value in record._asdict().items():
                json_object[field] = value
            json_array.append(json_object)
        LOGGER.debug(f"json_array: {json_array}")
        return json_array
    return None
