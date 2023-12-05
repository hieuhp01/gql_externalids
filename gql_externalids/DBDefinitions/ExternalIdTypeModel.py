import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class ExternalIdTypeModel(BaseModel):
    
    __tablename__ = "externalidtypes"

    id = UUIDColumn()
    name = Column(String, comment="name of externalid type")
    name_en = Column(String, comment="name of externalid type in English")
    urlformat = Column(String, comment="url of externalid type")

    category_id = Column(ForeignKey("externalidcategories.id"), index=True, nullable=True, comment="id of externalid's category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True, comment="who has created this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)