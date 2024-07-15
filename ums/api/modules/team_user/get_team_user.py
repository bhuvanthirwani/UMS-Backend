import logging
from ums.api.common.resource.crud import BaseResource
from ums.utils.exception import exception_handler
import ums.api.common.http_status as status
from .queries import find_users_by_role
from sqlalchemy.orm.exc import NoResultFound

LOGGER = logging.getLogger()

FIND_USER_ROLE_ENDPOINT = "/user-role"


class FindUserRoleResource(BaseResource):
    def __init__(self) -> None:
        super().__init__(
            dtype={
                "role_name": str
            }
        )

    @exception_handler
    def get(self):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query = self.req_args()
            role_name = query.get("role_name", None)
            print("role_name", role_name)
            json_res = []
            if role_name:
                json_res = find_users_by_role(role_name=role_name)

            return self.response(code=status.HTTP_200_OK, data=json_res)
        except NoResultFound:
            LOGGER.debug(f"No record found in {self.__entity_name__} & query - {query}")
            return self.response(code=status.HTTP_200_OK, data=[])
