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
    typeid_id = Column(ForeignKey("externalidtypes.id"), index=True, comment="id of the externalid's type")
    inner_id = UUIDFKey(nullable=True, comment="inner id of the entity")#Column(String, index=True)
    outer_id = Column(String, index=True, comment="outer id of the entity")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True, comment="who has created this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    
    