"""admin setup module."""

from flask import Flask
from flask_admin import Admin
from ums.settings import settings

from .views import admin_views
from .views.login import AdminLoginView
from .auth.rbac import register_rbac


def setup_admin(app: Flask):
    # app.config["FLASK_ADMIN_SWATCH"] = str(settings.admin_swatch)
    admin = Admin(
        app=app,
        name=settings.admin_name,
        template_mode=settings.admin_template,
        endpoint=settings.admin_endpoint,
        index_view=AdminLoginView(endpoint=settings.admin_endpoint),
        base_template="layout.html",
    )
    register_rbac(app=app)
    views = admin_views()
    admin.add_views(*views)
