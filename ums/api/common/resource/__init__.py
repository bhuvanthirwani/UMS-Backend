import logging
from flask import request
from flask_restful import Resource, abort
from ums.api.common.response import ApiResponse
from ums.utils.exception import PrimitiveDataAllowedException
import ums.api.common.http_status as status
from typing import Any, Union

LOGGER = logging.debug(__package__)


class BaseResource(Resource, ApiResponse):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.dtype: Union[dict, None] = None
        if dtype := kwargs.get("dtype", False):
            self.dtype = self._parse_dtype(dtype)

    @property
    def __entity_name__(self) -> str:
        return type(self).__name__

    @staticmethod
    def _parse_dtype(data) -> dict:
        assert isinstance(data, dict)
        ALLOW_TYPES = (int, str, float, bool)
        if not all(data[attr] in ALLOW_TYPES for attr in data):
            raise PrimitiveDataAllowedException(
                "Resource dtype must have primitive values only.",
            )
        return data

    def req_args(self) -> dict:
        """parse request args based on dtype config

        Returns:
            dict: Dictionary of args
        """
        if not self.dtype:
            return request.args.to_dict()

        _query = {}
        for attr in request.args.keys():
            dtype = self.dtype.get(attr, None)
            _query[attr] = request.args.get(attr, type=dtype)

        return _query

    def get_query_args(self, attribute: str, raise_error: bool = False) -> Any:
        """fetch query params from request args

        Args:
            attribute (str): key name
            raise_error (bool, optional): raise error if not present. Defaults to False.

        Returns:
            Any: value
        """
        data = self.req_args().get(attribute, None)
        if not data and raise_error:
            LOGGER.error(f"Missing key: {attribute} in {self.__entity_name__}")
            _res, code = self.response(
                code=status.HTTP_400_BAD_REQUEST,
                message=f"Key: {attribute} is missing in query params.",
            )
            abort(http_status_code=code, **_res)

        return data
