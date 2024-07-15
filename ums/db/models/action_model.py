import logging
from uuid import uuid4
from ums.db.base import ModelBase
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm.exc import NoResultFound
LOGGER = logging.getLogger(__package__)


class ActionModel(ModelBase):
    __tablename__ = "action"

    id = Column(
        UUID,
        primary_key=True,
        server_default=str(uuid4()),
        default=uuid4,
    )
    name = Column(String(), unique=True, nullable=False)

    # Define a one-to-many relationship with User
    # users = relationship("UserAccessModel", back_populates="roles")

    # Define a many-to-many relationship with Role

    def __repr__(self) -> str:
        return f"""
            name: {self.id} \n
            username: {self.name} \n
        """

    def find_by_name(self, name: str):
        try:
            # TODO: Remove extra query args that aren't present in self.model;
            query: dict = {}
            query["is_active"] = True
            query["name"] = name
            if len(query) > 0:
                entry: ActionModel = self.query.filter_by(**query).one_or_none()
            else:
                entry: ActionModel = self.query.one_or_none()

            # LOGGER.debug(f"status : {entry.id}")
            res = entry.id

            # LOGGER.debug(f"status_res : {type(res)}")

            return res
        except NoResultFound:
            return None
