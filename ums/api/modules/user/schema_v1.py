from marshmallow import Schema, fields, validate, post_load
from ums.db.models.access_model import UserAccessModel


class UserAccessSchema(Schema):
    id = fields.UUID(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1))
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.String(allow_none=True)
    phone = fields.String(required=True)
    internal_user = fields.Boolean(required=True)
    application = fields.String(required=True)
    last_login = fields.String(allow_none=True)

    @post_load
    def make_user_access(self, data, **kwargs):
        return UserAccessModel(**data)
