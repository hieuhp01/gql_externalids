from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_externalids.DBDefinitions import BaseModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_externalids.DBDefinitions import ExternalIdModel, ExternalIdTypeModel


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

resolveExternalIds = create1NGetter(ExternalIdModel, foreignKeyName="inner_id")
resolveExternalIdById = createEntityByIdGetter(ExternalIdModel)

resolveExternalTypeById = createEntityByIdGetter(ExternalIdTypeModel)
resolveExternalTypePaged = createEntityGetter(ExternalIdTypeModel)


async def resolveExternalIdIntoInnerId(session, externalid, typeid):
    """Resolver transformujici externi id daneho typu na interni id (uuid)"""
    stmt = select(ExternalIdModel).filter(
        ExternalIdModel.typeid_id == typeid, ExternalIdModel.outer_id == externalid
    )
    dbSet = await session.execute(stmt)
    result = next(dbSet.scalars(), None)
    return result


async def resolveInnerIdIntoExternalIds(session, internalid, typeid=None):
    """resolver transformujici interni id na viceprvkovy vektor externich id nebo na jednoprvkovy vektor
    je-li urcen typ externiho id, vraceny vektor muze byt prazdny, pokud nebylo nic nalezeno
    """
    if typeid is None:
        stmt = select(ExternalIdModel).filter(ExternalIdModel.inner_id == internalid)
    else:
        stmt = select(ExternalIdModel).filter(
            ExternalIdModel.typeid_id == typeid, ExternalIdModel.inner_id == internalid
        )

    dbSet = await session.execute(stmt)
    # result = list(map(lambda row: row.outer_id, dbSet.scalars()))
    return dbSet.scalars()


async def resolveAssignExternalId(session, internalid, externalid, typeid):
    """resolver prirazujici externi id daneho typu internimu id
    existuje-li takove prirazeni, je aktualizovano
    jinak je vytvoreno
    """
    stmt = select(ExternalIdModel).filter(
        ExternalIdModel.typeid_id == typeid, ExternalIdModel.inner_id == internalid
    )
    dbSet = await session.execute(stmt)
    dbRecord = next(dbSet.scalars(), None)
    if dbRecord is None:
        dbRecord = ExternalIdModel(
            typeid_id=typeid, inner_id=internalid, outer_id=externalid
        )

        session.add(dbRecord)
        await session.commit()  # session.flush()
    else:
        dbRecord.outer_id = externalid
        await session.commit()
    return dbRecord


# ...

import strawberry
import uuid
import datetime
import typing


UUIDType = uuid.UUID

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy("gql_externalids.GraphTypeDefinitions.externals")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy("gql_externalids.GraphTypeDefinitions.externals")]

@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="""Name """)
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""English name""")
def resolve_name_en(self) -> str:
    return self.name_en

@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created

async def resolve_user(user_id):
    from gql_externalids.GraphTypeDefinitions.externals import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result
    
@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(user_id=self.createdby)

@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(user_id=self.changedby)

# @strawberry.field(description="""Who made last change""")
# async def resolve_rbacobject(self) -> typing.Optional["UserGQLModel"]:
#     result = None if self.rbacobject is None else await resolve_user(self.rbacobject_id)
#     return result


resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update 
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object")
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


def createAttributeScalarResolver(
    scalarType: None = None, 
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
    ):

    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)
        
        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result
    return foreignkeyScalar

def createAttributeVectorResolver(
    scalarType: None = None, 
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10):

    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
        self, info: strawberry.types.Info,
        skip: int = skip,
        limit: int = limit,
        where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None
        
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result
    return foreignkeyVector

def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None
    @strawberry.field(description=description)
    async def by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result
    return by_id

def createRootResolver_by_page(
    scalarType: None, 
    whereFilterType: None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10):

    assert scalarType is not None
    assert whereFilterType is not None
    
    @strawberry.field(description=description)
    async def paged(
        self, info: strawberry.types.Info, 
        skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf)
        return result
    return paged
