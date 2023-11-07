import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer
)
from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class PublicationAuthorModel(BaseModel):
    
    __tablename__ = "publicationauthors"

    id = UUIDColumn()
    order = Column(Integer)
    share = Column(Integer)
    publication_id = Column(ForeignKey("publications.id"), index=True, nullable=True)
    user_id = Column(ForeignKey("users.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)