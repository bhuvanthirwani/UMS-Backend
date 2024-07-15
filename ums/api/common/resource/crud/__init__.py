import logging
import ums.api.common.http_status as status
from ums.utils.exception import exception_handler
from ums.db.base import Base
from marshmallow import Schema
from ums.api.common.resource import BaseResource
from ums.db import database
from sqlalchemy.orm.exc import NoResultFound
from ums.api.common.resource.validator import parse_rbody as validate_body
from typing import Union
from flask import request
LOGGER = logging.getLogger(__package__)


class CRUDResource(BaseResource):
    def __init__(self, model: Base, schema: Schema, **kwargs) -> None:
        self.model = model
        self.schema = schema
        super().__init__(**kwargs)

    @exception_handler
    def get(self):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query = self.req_args()
            query["is_active"] = True

            LOGGER.debug(f"Querying {query} for {self.__entity_name__}")
            if len(query) > 0:
                entires = self.model.query.filter_by(**query).all()
            else:
                entires = self.model.query.all()

            json_res = [self.schema.dump(entry) for entry in entires]
            return self.response(code=status.HTTP_200_OK, data=json_res)
        except NoResultFound:
            LOGGER.debug(f"No record found in {self.__entity_name__} & query - {query}")
            return self.response(code=status.HTTP_200_OK, data=[])

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

    @exception_handler
    def do_update(self, id: Union[str, int], update_obj: dict):
        item = self.model.query.get(id)
        if item:
            _ = [setattr(item, field, update_obj[field]) for field in update_obj]
            database.session.commit()
            return self.response(code=status.HTTP_200_OK, data=self.schema.dump(item))

        return self.response(
            code=status.HTTP_400_BAD_REQUEST,
            message=f"No record found in {self.__entity_name__}",
        )

    def put(self):
        data = request.get_json()
        _id = self.get_query_args(attribute="id", raise_error=True)
        return self.do_update(id=_id, update_obj=data)

    def delete(self):
        _id = self.get_query_args(attribute="id", raise_error=True)
        return self.do_update(id=_id, update_obj={"is_active": False})
