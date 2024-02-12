import strawberry
import datetime
import typing
from typing import Optional, List, Union, Annotated, Type
from gql_externalids.GraphPermissions import OnlyForAuthentized 
import gql_externalids.GraphTypeDefinitions
from uuid import UUID

from gql_externalids.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from gql_externalids.GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_lastchange,
    resolve_created,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
) 

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
# ProjectGQLModel = Annotated["ProjectGQLModel", strawberry.lazy(".externals")]
# PublicationGQLModel = Annotated["PublicationGQLModel", strawberry.lazy(".externals")]
# FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".externals")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external category id ()""",
)
class ExternalIdCategoryGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).externalcategoryids
    
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    # implementation is inherited

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject

#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

@createInputs
@dataclass
class ExternalIdCategoryWhereFilter:
    name: str
    name_en: str
    

externalid_category_page = createRootResolver_by_page(
    scalarType=ExternalIdCategoryGQLModel,
    whereFilterType=ExternalIdCategoryWhereFilter,
    description='Retrieves the externalid categories',
    loaderLambda=lambda info: getLoadersFromInfo(info).externalcategoryids
)


#####################################################################
#
# Mutation section
#
#####################################################################

import datetime

@strawberry.input()
class ExternalIdCategoryInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    id: Optional[UUID] = strawberry.field(default=None, description="Could be uuid primary key")
    createdby: strawberry.Private[UUID] = None

@strawberry.input()
class ExternalIdCategoryUpdateGQLModel:
    id: UUID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of category")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of category")
    changedby: strawberry.Private[UUID] = None
    
@strawberry.type()
class ExternalIdCategoryResultGQLModel:
    id: Optional[UUID] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of insert operation""")
    async def externalidcategory(self, info: strawberry.types.Info) -> Union[ExternalIdCategoryGQLModel, None]:
        result = await ExternalIdCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="defines a new external id category for an entity",
    permission_classes=[OnlyForAuthentized()])
async def externalidcategory_insert(self, info: strawberry.types.Info, externalidcategory: ExternalIdCategoryInsertGQLModel) -> ExternalIdCategoryResultGQLModel:
    actingUser = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).externalcategoryids
    externalidcategory.createdby = UUID(actingUser["id"])
    
    row = await loader.insert(externalidcategory)
    result = ExternalIdCategoryResultGQLModel(id=row.id,msg="ok") 
    result.id = row.id
    result.msg = "ok"

    return result

@strawberry.mutation(
    description="Update existing external id category for an entity",
    permission_classes=[OnlyForAuthentized()])
async def externalidcategory_update(self, info: strawberry.types.Info, externalidcategory: ExternalIdCategoryUpdateGQLModel) -> ExternalIdCategoryResultGQLModel:
    actingUser = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).externalcategoryids
    externalidcategory.changedby = UUID(actingUser["id"])
    
    result = ExternalIdCategoryResultGQLModel(id=externalidcategory.id,msg="ok")
    row = await loader.update(externalidcategory)
    result.id = None if row is None else row.id
    result.msg = "fail" if row is None else "ok"

    return result


