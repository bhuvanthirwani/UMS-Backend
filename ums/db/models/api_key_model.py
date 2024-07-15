# from sqlalchemy.orm import relationship
# from sqlalchemy import UUID, Column, ForeignKey, String, Text, Integer

# from ums.db.base import ModelBase
# from .user_model import UserAccessModel


# class ApiKeysModel(ModelBase):
#     __tablename__ = "api_key_details"

#     id = Column(UUID(), primary_key=True)
#     api_key = Column(Text(), unique=True, nullable=False)
#     scope_level = Column(Text(), nullable=True)
#     api_key = Column(String(), nullable=False)
#     rate_limit = Column(Integer(), nullable=False)
#     rate_limiting_window = Column(Integer(), nullable=False)


# class UserApiKeysModel(ModelBase):
#     __tablename__ = "user_api_keys"

#     id = Column(UUID(), primary_key=True)
#     key_id = Column(UUID(), ForeignKey("api_key_details.id"), nullable=False)
#     user_id = Column(UUID(), ForeignKey(UserAccessModel.id), nullable=False)

#     user = relationship(
#         UserAccessModel,
#         back_populates="user_api_keys",
#     )

#     api_key = relationship(
#         ApiKeysModel,
#         back_populates="user_api_keys",
#     )
