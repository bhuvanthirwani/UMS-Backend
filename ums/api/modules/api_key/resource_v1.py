# API Key resource
from ums.api.common import http_status
from ums.api.common.resource import BaseResource
from ums.utils.exception import exception_handler

# TODO: Fix needed for api_key relationship with users.
# from ums.db.models.api_key_model import ApiKeysModel

API_KEY_ENDPOINTS = "/api_keys"


class ApiKeyResource(BaseResource):
    def __init__(self) -> None:
        # self.schema = ApiKeysModel
        kwargs = {}
        super().__init__(**kwargs)

    @exception_handler
    def get(self) -> None:
        return self.response(code=http_status.HTTP_200_OK, data=None)

    @exception_handler
    def port(self) -> None:
        return self.response(code=http_status.HTTP_200_OK, data=None)

    @exception_handler
    def put(self) -> None:
        return self.response(code=http_status.HTTP_200_OK, data=None)
