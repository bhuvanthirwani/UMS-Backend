"""Customer admin view list"""

from .base import CustomAdminView
from ums.db.models.role_model import RolesModel
from ums.db.models.access_model import UserAccessModel


class RolesView(CustomAdminView):
    column_list = ["", "created_at", "updated_at", "deleted"]

    def __init__(self, **kwargs):
        super().__init__(model=RolesModel, **kwargs)


# class RolesView(CustomAdminView):
#     column_list = ["", "created_at", "updated_at", "deleted"]

#     def __init__(self, **kwargs):
#         super().__init__(model=RoleModel, **kwargs)


class UserAccessView(CustomAdminView):
    column_list = [
        "name",
        "username",
        "password",
        "email",
        "phone",
        "role_id",
        "role_id",
        "internal_user",
        "application",
        "last_login",
        "created_at",
        "updated_at",
        "deleted",
    ]

    def __init__(self, **kwargs):
        super().__init__(model=UserAccessModel, **kwargs)


custom_views = [
    RolesView(),
    # RolesView(),
    UserAccessView(),
]
