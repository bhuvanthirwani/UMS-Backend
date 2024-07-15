import logging
from ums.api.common.resource.crud import BaseResource
from ums.utils.exception import exception_handler
import ums.api.common.http_status as status
from .queries import find_resource_action_by_user
from sqlalchemy.orm.exc import NoResultFound

LOGGER = logging.getLogger()

FIND_USER_RESOURCE_ACTION_ENDPOINT = "/user-resource-permission"


class FindUserResourceActionResource(BaseResource):
    def __init__(self) -> None:
        super().__init__(
            dtype={
                "username": str
            }
        )

    @exception_handler
    def get(self):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query = self.req_args()
            username = query.get("username", None)
            print("username", username)
            json_res = []
            if username:
                json_res = find_resource_action_by_user(username=username)

            return self.response(code=status.HTTP_200_OK, data=json_res)
        except NoResultFound:
            LOGGER.debug(f"No record found in {self.__entity_name__} & query - {query}")
            return self.response(code=status.HTTP_200_OK, data=[])
