import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class GroupModel(BaseModel):
    __tablename__ = "groups"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    name = Column(String)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean, default=True)

    grouptype_id = Column(ForeignKey("grouptypes.id"), index=True)
    grouptype = relationship("GroupTypeModel", back_populates="groups")

    mastergroup_id = Column(ForeignKey("groups.id"), index=True)

    user = relationship("UserModel", back_populates="group", foreign_keys=[user_id])
    users = relationship("UserModel", back_populates="group")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

