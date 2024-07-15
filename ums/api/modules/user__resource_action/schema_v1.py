from marshmallow import Schema, fields, post_load
from ums.db.models.user_res_act_model import UserResourceActionModel

class UserResourceActionSchema(Schema):
    id = fields.UUID(required=False)
    user_id = fields.UUID(required=True)
    res_act_id = fields.UUID(required=True)

    @post_load
    def make_user_resource_action(self, data, **kwargs):
        return UserResourceActionModel(**data)
