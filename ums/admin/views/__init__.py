"""Admin view module"""
import logging

from typing import List
from importlib import import_module
from flask_admin.contrib.sqla import ModelView

from ums.db.models import get_model_list

from .create import create_view
from .custom import custom_views

LOGGER = logging.getLogger(__package__)


def admin_views(**kwargs) -> List[ModelView]:
    """
    Returns list of admin views for all app models.
    """
    views = []
    for _, name, _ in get_model_list():
        module = import_module(name)
        for module_attribute in dir(module):
            item = getattr(module, module_attribute)
            if (
                callable(item)
                and item.__module__ == name
                and "Model" in module_attribute
                and getattr(item, "__admin__", False)
            ):
                LOGGER.debug(f"Adding {item.__name__} to admin views")
                view = create_view(module=item)
                views.append(view)

    # Adding customer views.
    for view in custom_views:
        views.append(view)

    LOGGER.info(f"Total {len(views)} registered with admin.")
    return views
