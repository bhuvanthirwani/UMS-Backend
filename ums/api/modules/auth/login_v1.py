import base64
from datetime import datetime
import logging

from flask import request
from flask_jwt_extended import create_access_token

import ums.api.common.http_status as status
from ums.api.common.resource import BaseResource
from ums.db.models.access_model import UserAccessModel
from ums.utils import match_password
from ums.utils.exception import exception_handler
from ums.api.common.user_permission import (
    build_permission,
    user_resource_action_permission,
    find_user_roles_name
)

from .schema_v1 import LoginSchema

LOGGER = logging.getLogger(__package__)
AUTH_ENDPOINT = "/login"


class AuthResource(BaseResource):
    def __init__(self) -> None:
        self.schema = LoginSchema()
        self.DEFAULT_AUTH_MSG = "Username/password is not valid, Please try again"

    @staticmethod
    def valid_login_body(entry: dict) -> bool:
        if not isinstance(entry, dict):
            return False

        if (
            "user" not in entry
            or "password" not in entry
            or "application" not in entry
        ):
            return False

        return True

    @exception_handler
    def post(self):
        # entry = dict(request.get_json())
        entry = {}
        if request.authorization:
            # LOGGER.info("request.authorization: ", request.authorization, type(request.authorization))
            
            base64_part = str(request.authorization).split(' ')[1]
            decoded_bytes = base64.b64decode(base64_part)
            decoded_string = decoded_bytes.decode('utf-8')
            _details = decoded_string.split(":")
            entry["user"] = _details[0]
            entry["password"] = _details[1]
            entry["application"] = _details[2]
            
        # LOGGER.debug(f">> /v1/login data - {entry}")

        if not self.valid_login_body(entry):
            return self.response(
                code=status.HTTP_400_BAD_REQUEST,
                data=None,
                message=self.DEFAULT_AUTH_MSG,
            )

        try:
            user_entry = UserAccessModel.query.filter_by(
                username=entry.get("user"),
                application=entry.get("application"),
                
            ).one_or_none()
            if not user_entry:
                user_entry = UserAccessModel.query.filter_by(
                    email=entry.get("user"),
                    application=entry.get("application"),
                
                ).one_or_none()
            
            # LOGGER.info(f"User: {user_entry}")
            if not user_entry or not match_password(
                db_pswd=user_entry.password,
                password=entry.get("password"),
            ):
                return self.response(
                    code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    message=self.DEFAULT_AUTH_MSG,
                    success=False,
                    data=None,
                )
            user_resource_action_permission(user_entry.id)
            permission = build_permission(user_entry.id)
            if not permission:
                permission = {}

            claims = {
                "user_id": user_entry.id,
                "email": user_entry.email,
                "application": user_entry.application,
                "permission": permission,
                "user_roles": find_user_roles_name(user_entry.id),
                "exp": datetime.now().timestamp() + 86400*3
            }

            # LOGGER.info(f"User claims >> {claims}")
            token = create_access_token(identity=user_entry, additional_claims=claims)
            data = {"token": token}
            # LOGGER.success(f"User: {user_entry} logged in.")
            return self.response(
                code=status.HTTP_200_OK,
                data=data
            )
        except Exception as e:
            LOGGER.error(f"Error: {e}", exc_info=True)
            return self.response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                success=False,
                message=self.DEFAULT_AUTH_MSG,
            )
