from flask import Blueprint
from flask_restful import Api

from ..modules.auth.login_v1 import AuthResource, AUTH_ENDPOINT
from ..modules.user.resource_v1 import UserAccessResource, USER_ACCESS_ENDPOINT
from ..modules.role.resource_v1 import RolesResource, ROLES_ENDPOINT
from ..modules.role_user.resource_v1 import RoleUserResource, ROLE_USER_ENDPOINT
from ..modules.resource.resource_v1 import ResourceResource, RESOURCE_ENDPOINT
from ..modules.action.resource_v1 import ActionResource, ACTION_ENDPOINT
from ..modules.resource_action.resource_v1 import ResourceActionResource, RESOURCE_ACTION_ENDPOINT
from ..modules.user__resource_action.resource_v1 import UserResourceActionResource, USER_RESOURCE_ACTION_ENDPOINT
from ..modules.role__resource_action.resource_v1 import RoleResourceActionResource, ROLE_RESOURCE_ACTION_ENDPOINT
from ..modules.user__resource_action.grant_permission import GrantUserPermissionResource, GRANT_USER_PERMISSION_ENDPOINT
from ..modules.role_user.get_role_user import FindUserRoleResource, FIND_USER_ROLE_ENDPOINT
from ..modules.user__resource_action.get_user_resource_action import FindUserResourceActionResource, FIND_USER_RESOURCE_ACTION_ENDPOINT
from ..modules.resource_action.get_action_resource import FindResourceActionResource, FIND_ACTION_RESOURCE_ENDPOINT
from ..modules.role__resource_action.get_role_resource_action import FindRoleResourceActionResource, FIND_ROLE_RESOURCE_ACTION_ENDPOINT
from ..modules.role__resource_action.grant_permission import GrantRolePermissionResource, GRANT_ROLE_PERMISSION_ENDPOINT
# from ..modules.api_key.resource_v1 import ApiKeyResource, API_KEY_ENDPOINTS


def api_v1():
    v1_blueprint = Blueprint("v1_blueprint", __name__)
    v1_api = Api(v1_blueprint)

    v1_api.add_resource(AuthResource, AUTH_ENDPOINT)
    v1_api.add_resource(UserAccessResource, USER_ACCESS_ENDPOINT)
    v1_api.add_resource(RolesResource, ROLES_ENDPOINT)
    v1_api.add_resource(RoleUserResource, ROLE_USER_ENDPOINT)
    v1_api.add_resource(ResourceResource, RESOURCE_ENDPOINT)
    v1_api.add_resource(ActionResource, ACTION_ENDPOINT)
    v1_api.add_resource(ResourceActionResource, RESOURCE_ACTION_ENDPOINT)
    v1_api.add_resource(UserResourceActionResource, USER_RESOURCE_ACTION_ENDPOINT)
    v1_api.add_resource(RoleResourceActionResource, ROLE_RESOURCE_ACTION_ENDPOINT)
    v1_api.add_resource(GrantUserPermissionResource, GRANT_USER_PERMISSION_ENDPOINT)
    v1_api.add_resource(FindUserRoleResource, FIND_USER_ROLE_ENDPOINT)
    v1_api.add_resource(FindUserResourceActionResource, FIND_USER_RESOURCE_ACTION_ENDPOINT)
    v1_api.add_resource(FindResourceActionResource, FIND_ACTION_RESOURCE_ENDPOINT)
    v1_api.add_resource(FindRoleResourceActionResource, FIND_ROLE_RESOURCE_ACTION_ENDPOINT)
    v1_api.add_resource(GrantRolePermissionResource, GRANT_ROLE_PERMISSION_ENDPOINT)
    # v1_api.add_resource(ApiKeyResource, API_KEY_ENDPOINTS)
    return v1_blueprint
