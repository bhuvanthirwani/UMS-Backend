from marshmallow import Schema, fields, post_load
from ums.db.models.access_model import USERNAME_MIN_LENGTH, UserAccessModel


class LoginSchema(Schema):
    """
    User login Marshmallow Schema

    Marshmallow schema used for loading/dumping UserAccess
    """

    username = fields.String(
        allow_none=False,
        validate=lambda val: len(val) >= USERNAME_MIN_LENGTH,
    )
    password = fields.String(allow_none=False)

    @post_load
    def make_user_access(self, data):
        return UserAccessModel(**data)


class SignupSchema(Schema):
    """
    User signup Marshmallow Schema

    Marshmallow schema used for loading/dumping user signup
    """

    username = fields.String(
        allow_none=False,
        validate=lambda val: len(val) >= USERNAME_MIN_LENGTH,
    )
    password = fields.String(allow_none=False)
    role_id = fields.String(allow_none=False)
    role_id = fields.String(allow_none=False)

    @post_load
    def make_user_access(self, data):
        return UserAccessModel(**data)
