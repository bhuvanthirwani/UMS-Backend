import logging
import flask_login as login

from flask import url_for, redirect, request
from wtforms import form, fields, validators
from flask_admin import helpers, expose, AdminIndexView

from ums.db import database
from ums.admin.auth import AdminModel
from ums.db.utils.password import hash_password


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Invalid user")

        # we're comparing the plaintext pw with the the hash from the db
        if not bool(user.password == hash_password(self.password.data)):
            raise validators.ValidationError("Invalid password")

    def get_user(self):
        return (
            database.session.query(AdminModel).filter_by(login=self.login.data).first()
        )


# Create customized index view class that handles login & registration
class AdminLoginView(AdminIndexView):
    @expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            logging.debug("Redirecting unauthenticated user.")
            return redirect(url_for(".login_view"))
        return super(AdminLoginView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        self._template_args["form"] = form
        self._template_args["link"] = ""
        return super(AdminLoginView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))
