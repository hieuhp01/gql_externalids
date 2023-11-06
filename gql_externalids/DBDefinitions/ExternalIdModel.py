import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class ExternalIdModel(BaseModel):
    __tablename__ = "externalids"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    typeid_id = Column(ForeignKey("externalidtypes.id"), index=True)
    inner_id = UUIDFKey(nullable=True)#Column(String, index=True)
    outer_id = Column(String, index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    user = relationship("UserModel", back_populates="externalids", foreign_keys=[user_id])