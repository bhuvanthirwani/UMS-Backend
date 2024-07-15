from ums.db.models.role_model import RolesModel
from ums.db import database
from sqlalchemy import and_
def check_independent_resource_existence(model, filter):
    print("here")
    result = (
        database.session.query(
        model.id.label("id"),
        model.is_active.label("is_active")
        )
        .filter(
            and_(*filter)
        )
        .one_or_none()
    )
    print(f"check_independent_resource_existence: {result}")
    if result and len(result) > 0:
        return str(result[0]), str(result[1])
    return None, None
    