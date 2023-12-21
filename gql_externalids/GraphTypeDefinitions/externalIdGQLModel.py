import strawberry
import datetime
import typing
from typing import Union, Optional, List, Annotated
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
ProjectGQLModel = Annotated["ProjectGQLModel", strawberry.lazy(".externals")]
PublicationGQLModel = Annotated["PublicationGQLModel", strawberry.lazy(".externals")]
FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".externals")]

from .externalIdTypeGQLModel import ExternalIdTypeGQLModel

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdGQLModel(BaseGQLModel):
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


    @strawberry.field(description="""Inner id""")
    def inner_id(self) -> UUID:
        return self.inner_id

    @strawberry.field(description="""Outer id""")
    def outer_id(self) -> str:
        return self.outer_id

    @strawberry.field(description="""Type of id""")
    async def id_type(self, info: strawberry.types.Info) -> "ExternalIdTypeGQLModel":
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        return result

    @strawberry.field(description="""Type name of id""")
    async def type_name(self, info: strawberry.types.Info) -> Union[str, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info=info, id=self.typeid_id)
        if not result is None:
            result = result.name
        return result
    
#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(
    description="""Returns inner id based on external id type and external id value"""
    )
async def internal_id(
    self,
    info: strawberry.types.Info,
    typeid_id: UUID,
    outer_id: str,
) -> Union[UUID, None]:
    loader = getLoadersFromInfo(info).externalids
    rows = await loader.filter_by(outer_id=outer_id, typeid_id=typeid_id)
    row = next(rows, None)
    if row is None:
        return None
    else:
        return row.inner_id

@strawberry.field(
    description="""Returns outer ids based on external id type and inner id value"""
    )
async def external_ids(
    self,
    info: strawberry.types.Info,
    inner_id: UUID,
    typeid_id: Optional[UUID] = None,
) -> List[ExternalIdGQLModel]:
    loader = getLoadersFromInfo(info).externalids
    if typeid_id is None:
        rows = await loader.filter_by(inner_id=inner_id)
    else:
        rows = await loader.filter_by(inner_id=inner_id, typeid_id=typeid_id)
    return rows
    
#####################################################################
#
# Mutation section
#
#####################################################################

@strawberry.input()
class ExternalIdInsertGQLModel:
    inner_id: UUID = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: UUID = strawberry.field(default=None, description="Type of external id")
    outer_id: UUID = strawberry.field(default=None, description="Key used by other systems")
    changedby: strawberry.Private[UUID] = None
    createdby: strawberry.Private[UUID] = None

@strawberry.input()
class ExternalIdUpdateGQLModel:
    inner_id: UUID = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: Optional[UUID] = strawberry.field(default=None, description="Type of external id")
    outer_id: UUID = strawberry.field(default=None, description="Key used by other systems")
    
@strawberry.input()
class ExternalIdDeleteGQLModel:
    inner_id: strawberry.ID = strawberry.field(default=None, description="Primary key of entity which new outeid is assigned")
    typeid_id: strawberry.ID = strawberry.field(default=None, description="Type of external id")
    outer_id: strawberry.ID = strawberry.field(default=None, description="Key used by other systems")
    

@strawberry.type()
class ExternalIdResultGQLModel:
    id: Optional[UUID] = strawberry.field(default=None, description="Primary key of table row")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of drone operation""")
    async def externalid(self, info: strawberry.types.Info) -> Union[ExternalIdGQLModel, None]:
        result = await ExternalIdGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="defines a new external id for an entity")
async def externalid_insert(self, info: strawberry.types.Info, externalid: ExternalIdInsertGQLModel) -> ExternalIdResultGQLModel:
    actingUser = getUserFromInfo(info)
    loader = getLoadersFromInfo(info).externalids
    externalid.changedby = UUID(actingUser["id"])
    
    result = ExternalIdResultGQLModel()
    rows = await loader.filter_by(inner_id=externalid.inner_id, typeid_id=externalid.typeid_id, outer_id=externalid.outer_id)
    row = next(rows, None)
    if row is None:
        row = await loader.insert(externalid)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation(description="definies a new external id for an entity")
async def externalid_delete(self, info: strawberry.types.Info, externalid: ExternalIdDeleteGQLModel) -> ExternalIdResultGQLModel:
    loader = getLoadersFromInfo(info).externalids
    result = ExternalIdResultGQLModel()
    rows = await loader.filter_by(inner_id=externalid.inner_id, typeid_id=externalid.typeid_id, outer_id=externalid.outer_id)
    row = next(rows, None)
    if row is not None:
        row = await loader.delete(row.id)
        result.msg = "ok"
    else:
        result.id = None
        result.msg = "fail"
    return result

@strawberry.mutation(description="Updates an external ID with a new external ID")
async def externalid_update(self, info: strawberry.types.Info, externalid: ExternalIdUpdateGQLModel) -> ExternalIdResultGQLModel:
    loader = getLoadersFromInfo(info).externalids
    result = ExternalIdResultGQLModel()

    # Fetch the existing entity using the provided parameters
    rows = await loader.filter_by(inner_id=externalid.inner_id, outer_id=externalid.outer_id)
    row = next(rows, None)

    if row is not None:
        row.inner_id = externalid.inner_id
        row.typeid_id = externalid.typeid_id
        row.outer_id = externalid.outer_id
        
        await loader.update(row)

        result.msg = "ok"
        result.id = row.id
    else:
        result.id = None
        result.msg = "fail"

    return result