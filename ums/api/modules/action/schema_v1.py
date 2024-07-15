from marshmallow import Schema, fields, post_load
from ums.db.models.action_model import ActionModel

class ActionSchema(Schema):
    id = fields.UUID(required=False)
    name = fields.String(required=True)

    @post_load
    def make_action(self, data, **kwargs):
        return ActionModel(**data)
