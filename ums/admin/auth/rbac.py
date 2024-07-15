from flask import Flask
import flask_login as login

from ums.db import database
from ums.admin.auth import AdminModel


# Initialize flask-login
def register_rbac(app: Flask):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return database.session.query(AdminModel).get(user_id)
