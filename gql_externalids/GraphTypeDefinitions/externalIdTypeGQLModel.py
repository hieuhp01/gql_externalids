import strawberry
import datetime
import typing
from typing import Optional, Union, List, Annotated
from gql_externalids.GraphPermissions import OnlyForAuthentized, RoleBasedPermission
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
    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
) 


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
# ProjectGQLModel = Annotated["ProjectGQLModel", strawberry.lazy(".externals")]
# PublicationGQLModel = Annotated["PublicationGQLModel", strawberry.lazy(".externals")]
# FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".externals")]

ExternalIdCategoryGQLModel = Annotated["ExternalIdCategoryGQLModel", strawberry.lazy(".externalIdCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdTypeGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).externaltypeids
    
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


    @strawberry.field(description="""Category which belongs to""",permission_classes=[OnlyForAuthentized()])
    async def category(self, info: strawberry.types.Info) -> typing.Optional["ExternalIdCategoryGQLModel"]:
        from .externalIdCategoryGQLModel import ExternalIdCategoryGQLModel
        result = await ExternalIdCategoryGQLModel.resolve_reference(info, self.category_id)
        return result


#####################################################################
#
# Special fields for query
#
#####################################################################
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

@createInputs
@dataclass
class ExternalIdTypeWhereFilter:
    name: str
    name_en: str
    urlformat: str
    
    category_id: UUID

externalid_type_page = createRootResolver_by_page(
    scalarType=ExternalIdTypeGQLModel,
    whereFilterType=ExternalIdTypeWhereFilter,
    description='Retrieves the externalid types',
    loaderLambda=lambda info: getLoadersFromInfo(info).externaltypeids
)

@strawberry.field(description="""Rows of externaltypeids""",permission_classes=[OnlyForAuthentized()])
async def externalidtype_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[ExternalIdTypeGQLModel]:
    result = await ExternalIdTypeGQLModel.resolve_reference(info, id)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input()
class ExternalIdTypeInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    urlformat: Optional[str] = strawberry.field(default=None, description="Format for conversion of id into url link")
    id: Optional[UUID] = strawberry.field(default=None, description="Could be uuid primary key")
    category_id: Optional[UUID] = strawberry.field(default=None, description="Category of type")
    createdby: strawberry.Private[UUID] = None

@strawberry.input()
class ExternalIdTypeUpdateGQLModel:
    id: UUID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(default=None, description="Timestamp")
    name: Optional[str] = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(default=None, description="En name of type")
    urlformat: Optional[str] = strawberry.field(default=None, description="Format for conversion of id into url link")
    category_id: Optional[UUID] = strawberry.field(default=None, description="Category of type")
    changedby: strawberry.Private[UUID] = None
    
@strawberry.type()
class ExternalIdTypeResultGQLModel:
    id: Optional[UUID] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of insert operation""")
    async def externaltypeid(self, info: strawberry.types.Info) -> Union[ExternalIdTypeGQLModel, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="defines a new external type id for an entity",permission_classes=[OnlyForAuthentized()])
async def externaltypeid_insert(self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeInsertGQLModel) -> ExternalIdTypeResultGQLModel:
    actingUser = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).externaltypeids
    externaltypeid.createdby = UUID(actingUser["id"])
    
    row = await loader.insert(externaltypeid)
    result = ExternalIdTypeResultGQLModel(id=row.id,msg="ok")
    result.id = row.id
    result.msg = "ok"

    return result

@strawberry.mutation(description="Update existing external type id for an entity",permission_classes=[OnlyForAuthentized()])
async def externaltypeid_update(self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeUpdateGQLModel) -> ExternalIdTypeResultGQLModel:
    actingUser = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).externaltypeids
    externaltypeid.changedby = UUID(actingUser["id"])
    
    result = ExternalIdTypeResultGQLModel(id=externaltypeid.id,msg="ok")
    row = await loader.update(externaltypeid)
    result.id = None if row is None else row.id
    result.msg = "fail" if row is None else "ok"
    
    return result

