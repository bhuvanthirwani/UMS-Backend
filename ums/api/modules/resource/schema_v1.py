from marshmallow import Schema, fields, post_load
from ums.db.models.resource_model import ResourceModel


class ResourceSchema(Schema):
    id = fields.UUID(required=False)
    name = fields.String(required=True)

    @post_load
    def make_resource(self, data, **kwargs):
        return ResourceModel(**data)
