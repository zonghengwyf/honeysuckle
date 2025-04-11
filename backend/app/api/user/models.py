
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.base.db import ModelBase

class User(ModelBase):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # 通过 user_roles 关联到 Role
    roles = relationship("Role", secondary="user_roles")

class Role(ModelBase):
    __tablename__ = "roles"
    name = Column(String, unique=True, index=True)

    # 关联用户
    users = relationship("User", secondary="user_roles")

class Permission(ModelBase):
    __tablename__ = "permissions"
    name = Column(String, unique=True, index=True)

    # 关联角色
    roles = relationship("Role", secondary="role_permissions")

class UserRole(ModelBase):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

class RolePermission(ModelBase):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)