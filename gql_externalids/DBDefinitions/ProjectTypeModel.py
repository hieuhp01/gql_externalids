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

class ProjectTypeModel(BaseModel):
    __tablename__ = "projecttypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    category_id = Column(ForeignKey("projectcategories.id"), index=True, nullable=True)
    projects = relationship("ProjectModel", back_populates="projecttype")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)