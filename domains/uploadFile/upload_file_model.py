from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database.db import Base
from common.consts.timestamps import Timestamps
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class UploadFileModel(Base, Timestamps):
    __tablename__ = "upload_files"

    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(String(50), nullable=False)
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    owner = relationship("UserModel", back_populates="profile_image")
