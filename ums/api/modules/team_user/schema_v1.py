from marshmallow import Schema, fields, post_load
from ums.db.models.role_user_model import RoleUserModel

class RoleUserSchema(Schema):
    id = fields.UUID(required=False)
    role_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)

    @post_load
    def make_role_user(self, data, **kwargs):
        return RoleUserModel(**data)
