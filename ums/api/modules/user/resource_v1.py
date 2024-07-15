import json
import logging
import uuid
from flask import Flask, request, jsonify
import requests
from ums.settings import settings
from .schema_v1 import UserAccessSchema
from ums.db.models.access_model import UserAccessModel
from ums.api.common.resource.crud import CRUDResource
from typing import Union
from ums.utils.exception import exception_handler
from ums.db import database
from ums.api.common.resource.validator import parse_rbody as validate_body
from ums.api.common.check_existence import check_independent_resource_existence
import ums.api.common.http_status as status
from ums.api.common import constants

LOGGER = logging.getLogger(__package__)


USER_ACCESS_ENDPOINT = "/user-access"


class UserAccessResource(CRUDResource):
    def __init__(self) -> None:
        schema = UserAccessSchema()
        super().__init__(model=UserAccessModel, schema=schema, dtype={"name": str, "username": str, "password": str, "email": str, "phone": str, "internal_user": bool, "application": str})

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
        filter.append(UserAccessModel.username == entry.username)
        existing_id, is_acitve = check_independent_resource_existence(UserAccessModel, filter)
        print(f"existing_id: {existing_id}, is_active: {is_acitve}")
        if existing_id:
            if is_acitve == "False":
                return self.response(
                    code=status.HTTP_400_BAD_REQUEST, message=f"User with {entry.username} already exists, but is not in active state request admin to re-active or create role with a different name"
                )
            else:
                return self.response(code=status.HTTP_400_BAD_REQUEST, message=f"User with {entry.username} already exists")

        entry.id = str(uuid.uuid4())
        request = {"id": entry.id, "name": entry.name, "email": entry.email}

        url = None
        headers = None
        if entry.application == "app1":
            request["phone_number"] = entry.phone
            request["username"] = entry.username
            LOGGER.info(f"request info -----{request}")
            url = settings.app2_user_url
            headers = constants.CREATE_APP_USER_HEADER  # Set appropriate headers if needed

        if url and headers and (entry.application == "deadler" or entry.application == "app2"):
            LOGGER.debug("inside if statement to check url and headers")
            try:
                response = requests.post(url, json=request, headers=headers)  # call a second api from here
                if response.status_code == status.HTTP_201_CREATED:
                    LOGGER.success(f"record saved successfully {response}")
                else:
                    return self.response(code=response.status_code, data="failed to call second api-endpoint")
            except requests.exceptions.RequestException as e:
                # Handle exceptions such as network errors
                return self.response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)
                # return jsonify({'success': False, 'error': str(e)})

        try:
            database.session.add(entry)
            database.session.commit()
        except Exception as e:
            LOGGER.error(f"Error: {e}", exc_info=True)
            return self.response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=e)

        return self.response(
            code=status.HTTP_201_CREATED,
            data=self.schema.dump(entry),
            message=f"Created successfully.",
        )

    def delete(self):
        _username = self.get_query_args(attribute="username", raise_error=True)
        return self.do_update(username=_username, update_obj={"is_active": False})

    @exception_handler
    def do_update(self, username: Union[str, str], update_obj: dict):
        item = self.model.query.filter(self.model.username == username).one_or_none()
        if item:
            _ = [setattr(item, field, update_obj[field]) for field in update_obj]
            database.session.commit()
            return self.response(code=status.HTTP_200_OK, data=self.schema.dump(item))

        return self.response(
            code=status.HTTP_400_BAD_REQUEST,
            message=f"No record found in {self.__entity_name__}",
        )
