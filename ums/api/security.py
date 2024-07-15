import logging
from typing import Union
from datetime import timedelta
from flask import Flask, jsonify
from ums.settings import settings
from ums.api.common.response import ApiResponse
from ums.api.common import http_status
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)

jwt_manager: Union[JWTManager, None] = None
LOGGER = logging.getLogger(__package__)


def setup_authorization(app: Flask) -> None:
    global jwt_manager
    # ? OPTS : https://flask-jwt-extended.readthedocs.io/en/stable/options.html
    app.config["JWT_SECRET_KEY"] = str(settings.jwt_secret)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=settings.jwt_expiry_hours)
    jwt_manager = JWTManager(app=app)

    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    @jwt_manager.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    resp = ApiResponse()

    # Custom unauthorized response
    @jwt_manager.unauthorized_loader
    def unauthorized_response(callback):
        return resp.response(
            code=http_status.HTTP_401_UNAUTHORIZED,
            data=None,
            message="You are not authorized.",
        )

    # ? DOCS: https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading.html # noqa
    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    # @jwt_manager.user_lookup_loader
    # def user_lookup_callback(_jwt_header, jwt_data):
    #     identity = jwt_data["sub"]
    #     return User.query.filter_by(id=identity).one_or_none()

    LOGGER.info("Api authorization enforced.")


if __name__ == "__main__":
    # Sample usage
    @jwt_required()
    def protected():
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )
