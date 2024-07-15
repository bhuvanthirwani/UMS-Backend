from marshmallow import Schema, fields, post_load
from ums.db.models.role_res_act_model import RoleResourceActionModel

class RoleResourceActionSchema(Schema):
    id = fields.UUID(required=False)
    role_id = fields.UUID(required=True)
    res_act_id = fields.UUID(required=True)

    @post_load
    def make_role_resource_action(self, data, **kwargs):
        return RoleResourceActionModel(**data)
