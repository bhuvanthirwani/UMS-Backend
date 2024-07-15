from .schema_v1 import RoleResourceActionSchema
from ums.db.models.role_res_act_model import RoleResourceActionModel
from ums.api.common.resource.crud import CRUDResource
ROLE_RESOURCE_ACTION_ENDPOINT = "/role-resource-action"


class RoleResourceActionResource(CRUDResource):
    def __init__(self) -> None:
        schema = RoleResourceActionSchema()
        super().__init__(
            model=RoleResourceActionModel,
            schema=schema,
            dtype={
                "id": str,
                "role_id": str,
                "res_act_id": str
            },
        )