from marshmallow import Schema, fields, post_load
from ums.db.models.resource_action_model import ResourceActionModel

class ResourceActionSchema(Schema):
    id = fields.UUID(required=False)
    resource_id = fields.UUID(required=True)
    action_id = fields.UUID(required=True)

    @post_load
    def make_resource_action(self, data, **kwargs):
        return ResourceActionModel(**data)
