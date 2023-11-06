import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class UserModel(BaseModel):

    __tablename__ = "users"

    id = UUIDColumn()
    group_id = Column(ForeignKey("groups.id"), index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)

    group = relationship("GroupModel", back_populates="users", foreign_keys=[group_id])
    externalids = relationship("ExternalIdModel", back_populates="user", foreign_keys="ExternalIdModel.users_id")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


