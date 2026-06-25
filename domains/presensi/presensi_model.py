import uuid
from sqlalchemy import Column, String, ForeignKey, Table, Text, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())

class 
class PresensiModel(Base, Timestamps):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    idRole = Column(String)
    latitude = Column(String(39))
    logitude = Column(String())
