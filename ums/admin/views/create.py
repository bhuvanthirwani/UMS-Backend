"""Creating admin view"""

from ums.db import database
from flask_admin.contrib.sqla import ModelView
import flask_login as login


class AdminModelView(ModelView):
    page_size = 50
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    column_hide_backrefs = False
    column_exclude_list = ["password"]

    def is_accessible(self):
        return login.current_user.is_authenticated


def create_view(module, **kwargs) -> ModelView:
    return AdminModelView(model=module, session=database.session, **kwargs)
