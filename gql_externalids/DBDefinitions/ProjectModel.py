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

class ProjectModel(BaseModel):
    __tablename__ = "projects"

    id = UUIDColumn()

    name = Column(String)
    startdate = Column(DateTime)
    enddate = Column(DateTime)

    projecttype_id = Column(ForeignKey("projecttypes.id"), index=True)
    projecttype = relationship("ProjectTypeModel", back_populates="projects")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    group_id = Column(ForeignKey("groups.id"), index=True)
    group = relationship("GroupModel", backref="projects")