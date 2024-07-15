import logging
from .schema_v1 import ActionSchema
from ums.db.models.action_model import ActionModel
from ums.api.common.resource.crud import CRUDResource
from typing import Union
from ums.utils.exception import exception_handler
from ums.api.common.resource.validator import parse_rbody as validate_body
from ums.api.common.check_existence import check_independent_resource_existence
from ums.db import database
import ums.api.common.http_status as status
LOGGER = logging.getLogger(__package__)


ACTION_ENDPOINT = "/action"


class ActionResource(CRUDResource):
    def __init__(self) -> None:
        schema = ActionSchema()
        super().__init__(
            model=ActionModel,
            schema=schema,
            dtype={
                "id": str,
                "name": str
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
        filter.append(ActionModel.name == entry.name)
        existing_id, is_acitve = check_independent_resource_existence(ActionModel, filter)
        print(f"existing_id: {existing_id}, is_active: {is_acitve}")
        if existing_id:
            if is_acitve == 'False':
                return self.response(code=status.HTTP_400_BAD_REQUEST, message=f"Action with name {entry.name} already exists, but is not in active state request admin to re-active or create action with a different name")
            else:
                return self.response(code=status.HTTP_400_BAD_REQUEST, message=f"Action with name {entry.name} already exists")
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
      

    def delete(self):
        _name = self.get_query_args(attribute="name", raise_error=True)
        LOGGER.debug(f"name: {_name}")
        return self.do_update(name=_name, update_obj={"is_active": False})

    @exception_handler
    def do_update(self, name: Union[str, str], update_obj: dict):
        item = self.model.query.filter(self.model.name == name).one_or_none()
        if item:
            _ = [setattr(item, field, update_obj[field]) for field in update_obj]
            database.session.commit()
            return self.response(code=status.HTTP_200_OK, data=self.schema.dump(item))

        return self.response(
            code=status.HTTP_400_BAD_REQUEST,
            message=f"No record found in {self.__entity_name__}",
        )
