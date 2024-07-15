import logging
from ums.api.common.resource.crud import BaseResource
from ums.utils.exception import exception_handler
import ums.api.common.http_status as status
from .queries import find_action_by_resource
from sqlalchemy.orm.exc import NoResultFound

LOGGER = logging.getLogger()

FIND_ACTION_RESOURCE_ENDPOINT = "/action-resource"


class FindResourceActionResource(BaseResource):
    def __init__(self) -> None:
        super().__init__(
            dtype={
                "resource_name": str
            }
        )

    @exception_handler
    def get(self):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query = self.req_args()
            resource_name = query.get("resource_name", None)
            print("resource_name", resource_name)
            json_res = []
            if resource_name:
                json_res = find_action_by_resource(resource_name=resource_name)

            return self.response(code=status.HTTP_200_OK, data=json_res)
        except NoResultFound:
            LOGGER.debug(f"No record found in {self.__entity_name__} & query - {query}")
            return self.response(code=status.HTTP_200_OK, data=[])
