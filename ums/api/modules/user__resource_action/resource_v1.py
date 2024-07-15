# from typing import Union
# from ums.utils.exception import exception_handler
# from ums.db import database
# import ums.api.common.http_status as status


from .schema_v1 import UserResourceActionSchema
from ums.api.common.resource.crud import CRUDResource
from ums.db.models.user_res_act_model import UserResourceActionModel


USER_RESOURCE_ACTION_ENDPOINT = "/user-resource-action"


class UserResourceActionResource(CRUDResource):
    def __init__(self) -> None:
        schema = UserResourceActionSchema()
        super().__init__(
            model=UserResourceActionModel,
            schema=schema,
            dtype={
                "id": str,
                "user_id": str,
                "res_act_id": str
            },
        )
