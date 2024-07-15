import logging
from flask_restful import abort

import ums.api.common.http_status as status
from ums.api.common.response import ApiResponse

response = ApiResponse()


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = getattr(e, "message", repr(e))
            data, code = response.response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=message,
            )
            if code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                logging.error(e, exc_info=True)
            else:
                logging.warning(e)

            abort(http_status_code=code, **data)

    return wrapper

from werkzeug.exceptions import HTTPException


class PrimitiveDataAllowedException(Exception):
    ...


class APIException(HTTPException):
    def __init__(self, code, message):
        super().__init__()
        self.code = code
        self.description = message
