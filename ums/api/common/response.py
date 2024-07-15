from typing import Any, Dict, Optional

import ums.api.common.http_status as status


class ApiResponse:
    """API response generator"""

    @staticmethod
    def __message(code: int, message: str):
        if message != "ok":
            return message

        if code == status.HTTP_404_NOT_FOUND:
            message = "OOPS! We couldn't find what you are looking for."
        elif code == status.HTTP_401_UNAUTHORIZED:
            message = "You are not authorized."
        elif code == status.HTTP_400_BAD_REQUEST:
            message = "OOPS! Something is not right, please check."

        if status.is_server_error(code):
            message = "Something went wrong, we looking into it."

        return message

    @staticmethod
    def __did_success(code: int) -> bool:
        """return success for a given response

        Args:
            code (int): HTTP Status code

        Returns:
            bool: True | False
        """
        return not (
            status.is_client_error(code)
            or status.is_server_error(code)
            or code == status.HTTP_304_NOT_MODIFIED
        )

    def response(self, code: int, data: Any = None, headers: Optional[Dict[str, str]] = None, **kwargs):
        """create Structured API response

        Args:
            code (int): HTTP status code
            data (Any, optional): data to be send in response. Defaults to None.

        Returns:
            tuple: data, status_code.
        """
        success: bool = kwargs.pop("success", self.__did_success(code))
        message: str = self.__message(code, kwargs.pop("message", "ok"))

        if "InvalidRequestError" in message:
            code = status.HTTP_400_BAD_REQUEST

        response_body = {
            "success": success,
            "message": message,
            "data": data,
            "extras": kwargs,
        }
        if headers:
            return response_body, code, headers
        else:
            return response_body, code
