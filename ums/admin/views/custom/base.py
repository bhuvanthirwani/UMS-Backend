import flask_login as login
from ums.db import database
from flask_admin.contrib.sqla import ModelView


class CustomAdminView(ModelView):
    page_size = 50
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"
    column_hide_backrefs = False
    column_display_all_relations = True
    column_hide_backrefs = False

    def __init__(self, model, **kwargs):
        super().__init__(model=model, session=database.session, **kwargs)

    def is_accessible(self):
        return login.current_user.is_authenticated
