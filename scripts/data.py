"""Script to load the test data into the tables."""

import logging
import random
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ums.db.base import Base
from ums.db.models.role_model import RolesModel
from ums.db.models.access_model import UserAccessModel
from ums.db.models.role_user_model import RoleUserModel
from ums.db.models.resource_model import ResourceModel
from ums.db.models.action_model import ActionModel
from ums.db.models.resource_action_model import ResourceActionModel
from ums.db.models.user_res_act_model import UserResourceActionModel
from ums.db.models.role_res_act_model import RoleResourceActionModel
from ums.settings import settings

DATABASE_URL = str(settings.db_url)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
session = Session()


def create_dummy_users(session):
    dummy_users = [
        UserAccessModel(
            id=uuid4(),
            name=f"User{i}",
            username=f"user{i}",
            password=f"password{i}",
            email=f"user{i}@example.com",
            phone=1234567890 + i + "",
            internal_user=False,
            application=random.choice(["app1", "app2", "app3", "app4"]),
            last_login=datetime.now(),
        )
        for i in range(1, 6)
    ]

    session.add_all(dummy_users)
    user_id = []
    for user in dummy_users:
        user_id.append(user.id)
    
    return user_id


# Function to create dummy entries for RolesModel
def create_dummy_roles(session) -> list[str]:
    dummy_roles = [RolesModel(id=uuid4(), name=f"Role{i}") for i in range(1, 6)]
    roles = [str(role.id) for role in dummy_roles]

    session.add_all(dummy_roles)
    return roles


def create_dummy_role_user_association(session, roles: list[str], user: list[str]):
    dummy_role_user_association = [
        RoleUserModel(id=uuid4(), role_id=roles[0], user_id=user[0]),
        RoleUserModel(id=uuid4(), role_id=roles[0], user_id=user[1]),
        RoleUserModel(id=uuid4(), role_id=roles[0], user_id=user[2]),
        RoleUserModel(id=uuid4(), role_id=roles[1], user_id=user[2]),
        RoleUserModel(id=uuid4(), role_id=roles[1], user_id=user[3]),
        RoleUserModel(id=uuid4(), role_id=roles[2], user_id=user[0]),
    ]
    session.add_all(dummy_role_user_association)

def create_dummy_resource(session):
    dummy_resource = [
        ResourceModel(
            id=uuid4(),
            name=f"Resource{i}"
        )
        for i in range(1, 6)
    ]
    session.add_all(dummy_resource)
    resource: list = []
    for res in dummy_resource:
        resource.append(res.id)
    return resource
# Function to create dummy entries for RoleModel

def create_dummy_action(session):
    dummy_action = [
        ActionModel(
            id=uuid4(),
            name=f"Action{i}"
        )
        for i in range(1, 6)
    ]
    session.add_all(dummy_action)
    action: list = []
    for act in dummy_action:
        action.append(act.id)
    return action

def create_dummy_resource_action_association(session, resource: list[str], action: list[str]):
    dummy_resource_action = [
        ResourceActionModel(id=uuid4(), resource_id = resource[0], action_id=action[0]),
        ResourceActionModel(id=uuid4(), resource_id = resource[0], action_id=action[1]),
        ResourceActionModel(id=uuid4(), resource_id = resource[0], action_id=action[2]),
        ResourceActionModel(id=uuid4(), resource_id = resource[1], action_id=action[3]),
        ResourceActionModel(id=uuid4(), resource_id = resource[1], action_id=action[4])
    ]
    session.add_all(dummy_resource_action)
    resource_action: list = []
    for res_act in dummy_resource_action:
        resource_action.append(res_act.id)
    return resource_action

def create_dummy_user__resource_action_association(session, user:list[str], resource_action: list[str]):
    dummy_user__resource_action_association = [
        UserResourceActionModel(id=uuid4(), user_id=user[0], res_act_id=resource_action[0]),
        UserResourceActionModel(id=uuid4(), user_id=user[0], res_act_id=resource_action[1]),
        UserResourceActionModel(id=uuid4(), user_id=user[0], res_act_id=resource_action[2]),
        UserResourceActionModel(id=uuid4(), user_id=user[1], res_act_id=resource_action[1]),
        UserResourceActionModel(id=uuid4(), user_id=user[2], res_act_id=resource_action[3]),
        UserResourceActionModel(id=uuid4(), user_id=user[2], res_act_id=resource_action[2]),
        UserResourceActionModel(id=uuid4(), user_id=user[3], res_act_id=resource_action[2]),
        UserResourceActionModel(id=uuid4(), user_id=user[3], res_act_id=resource_action[1]),

    ]
    session.add_all(dummy_user__resource_action_association)

def create_dummy_role__resource_action_association(session, roles:list[str], resource_action: list[str]):
    dummy_role__resource_action_association = [
        RoleResourceActionModel(id=uuid4(), role_id=roles[0], res_act_id=resource_action[0]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[0], res_act_id=resource_action[1]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[0], res_act_id=resource_action[2]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[1], res_act_id=resource_action[1]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[2], res_act_id=resource_action[3]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[2], res_act_id=resource_action[2]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[3], res_act_id=resource_action[2]),
        RoleResourceActionModel(id=uuid4(), role_id=roles[3], res_act_id=resource_action[1]),

    ]
    session.add_all(dummy_role__resource_action_association)
# Function to create dummy entries for RoleRolesAssociation



if __name__ == "__main__":
    logging.info("Created tables in DB.")
    try:
        roles = create_dummy_roles(session=session)
        user = create_dummy_users(session=session)
        session.commit()
        create_dummy_role_user_association(session=session, user=user, roles=roles)
        resource = create_dummy_resource(session=session)
        action = create_dummy_action(session=session)
        session.commit()
        res_act = create_dummy_resource_action_association(session=session, resource=resource, action=action)
        session.commit()
        create_dummy_user__resource_action_association(session=session, resource_action=res_act, user=user)
        create_dummy_role__resource_action_association(session=session, resource_action=res_act, roles=roles)
        session.commit()
        session.close()
        
        print("Data seeded successfully.")
    except Exception:
        logging.error("Failed to created error", exc_info=True)
        session.rollback()
        session.close()
