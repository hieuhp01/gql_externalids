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

class PublicationTypeModel(BaseModel):
    
    __tablename__ = "publicationtypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    category_id = Column(ForeignKey("publicationcategories.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)