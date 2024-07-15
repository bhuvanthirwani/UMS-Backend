import logging
from .schema_v1 import UserResourceActionSchema
from ums.api.common.resource.crud import BaseResource
from ums.utils.exception import exception_handler
from ums.api.common.check_existence import check_independent_resource_existence
from flask import request
from ums.db import database
import ums.api.common.http_status as status
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from ums.db.models.resource_action_model import ResourceActionModel
from ums.db.models.user_res_act_model import UserResourceActionModel
from typing import Union

LOGGER = logging.getLogger()

GRANT_USER_PERMISSION_ENDPOINT = "/user-permission"


class GrantUserPermissionResource(BaseResource):
    def __init__(self) -> None:
        self.schema = UserResourceActionSchema()
        self.model = UserResourceActionModel()

    @exception_handler
    def post(self):
        entry = dict(request.get_json())
        user_id = entry.get('user_id', None)
        resource_name = entry.pop("resource_name", None)
        action_name = entry.pop("action_name", None)
        print("data: ", resource_name, action_name)
        res_id = None
        action_id = None
        res_act_id = None
        if resource_name:
            res_id = ResourceModel().find_by_name(resource_name)
            print("res_id", res_id)
        if action_name:
            action_id = ActionModel().find_by_name(action_name)
            print("act_id", action_id)
        if res_id and action_id:
            res_act_id = ResourceActionModel().find_by_resource_action_id_pair(res_id, action_id)
            print("res_act_id", res_act_id)
        data: dict = {}
        if res_act_id and user_id:
            filter = []
            filter.append(UserResourceActionModel.res_act_id == res_act_id)
            filter.append(UserResourceActionModel.user_id == user_id)
            existing_id, is_acitve = check_independent_resource_existence(UserResourceActionModel, filter)
            print(f"existing_id: {existing_id}, is_active: {is_acitve}")
            if existing_id:
                if is_acitve == 'False':
                    return self.do_update(existing_id, update_obj={"is_active": True})
                else:
                    return self.response(code=status.HTTP_400_BAD_REQUEST, message=f"Requested permission for the user already exists")
            data = UserResourceActionModel(user_id=user_id, res_act_id=res_act_id)
            print("data", data)
        try:
            database.session.add(data)
            database.session.commit()
        except Exception as e:
            LOGGER.error(f"Error: {e}", exc_info=True)
            return self.response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                success=False,
                message="Something went wrong!",
            )

    @exception_handler
    def do_update(self, id: Union[str, int], update_obj: dict):
        item = self.model.query.get(id)
        if item:
            _ = [setattr(item, field, update_obj[field]) for field in update_obj]
            database.session.commit()
            return self.response(code=status.HTTP_200_OK, data=self.schema.dump(item))

        return self.response(
            code=status.HTTP_400_BAD_REQUEST,
            message=f"No record found in {self.__entity_name__}",
        )
