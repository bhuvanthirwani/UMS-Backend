import logging
from ums.api.common.resource.crud import CRUDResource
from .schema_v1 import ResourceActionSchema
from ums.db.models.resource_action_model import ResourceActionModel
from ums.utils.exception import exception_handler
from ums.api.common.resource.validator import parse_rbody as validate_body
from ums.api.common.check_existence import check_independent_resource_existence
LOGGER = logging.getLogger(__package__)
from ums.db import database
import ums.api.common.http_status as status


RESOURCE_ACTION_ENDPOINT = "/resource-action"


class ResourceActionResource(CRUDResource):
    def __init__(self) -> None:
        schema = ResourceActionSchema()
        super().__init__(
            model=ResourceActionModel,
            schema=schema,
            dtype={
                "id": str,
                "resource_id": str,
                "action_id": str
            },
        )
    

    @exception_handler
    def post(self):
        entry, error = validate_body(self.schema)
        if not entry or error:
            LOGGER.warning(f"Deserialization failed for {self.__entity_name__}")
            return self.response(
                code=status.HTTP_400_BAD_REQUEST,
                data=str(error),
                success=False,
                message="Validation failed while creating entry",
            )
        print("here")
        filter = []
        filter.append(ResourceActionModel.resource_id == entry.resource_id)
        filter.append(ResourceActionModel.action_id == entry.action_id)
        existing_id, is_acitve = check_independent_resource_existence(ResourceActionModel, filter)
        print(f"existing_id: {existing_id}, is_active: {is_acitve}")
        if existing_id:
            if is_acitve == 'False':
                return super().do_update(existing_id, update_obj={"is_active": True})
            else:
                return self.response(code=status.HTTP_400_BAD_REQUEST, message=f"Permission mapping already exists")
        try:
            database.session.add(entry)
            database.session.commit()
        except Exception as e:
            LOGGER.error(f"Error: {e}", exc_info=True)
            return self.response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)

        LOGGER.success(f"record saved {self.__entity_name__} successfully")
        return self.response(
            code=status.HTTP_201_CREATED,
            data=self.schema.dump(entry),
            message="Created successfully.",
        )
    