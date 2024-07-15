from marshmallow import Schema, fields, validate, post_load
from ums.db.models.role_model import RolesModel


class RoleSchema(Schema):
    id = fields.UUID(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1))

    @post_load
    def make_roles(self, data, **kwargs):
        return RolesModel(**data)
