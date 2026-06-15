import uuid
from sqlalchemy import Column, String, ForeignKey, Table, Text, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


user_roles_association = Table(
    "user_roles_association",
    Base.metadata,
    Column(
        "user_id",
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class RoleModel(Base, Timestamps):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    name = Column(String(50), unique=True, nullable=False, index=True)

    users = relationship(
        "UserModel", secondary=user_roles_association, back_populates="roles"
    )


class UserModel(Base, Timestamps):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nomor_telepon = Column(String(20), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    roles = relationship(
        "RoleModel", secondary=user_roles_association, back_populates="users"
    )
    profile_image = relationship(
        "UploadFileModel",
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
    )
