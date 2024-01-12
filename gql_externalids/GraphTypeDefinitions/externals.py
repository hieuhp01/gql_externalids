import strawberry
from typing import List
from uuid import UUID

from .externalIdGQLModel import ExternalIdGQLModel

from gql_externalids.utils.Dataloaders import getLoadersFromInfo

###########################################################################################################################
#
# zde definujte sve rozsirene GQL modely,
# ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
# venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
# vsimnete si,
# - jak je definovan dekorator tridy (extend=True)
# - jaky dekorator je pouzit (federation.type)
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
# - ma odlisnou implementaci v porovnani s modelem, za ktery jste odpovedni
#
###########################################################################################################################
@strawberry.field(description="""All external ids related to the entity""")
async def resolve_external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
    ##loader = getLoaders(info=info).externalids_inner_id
    ##result = await loader.load(self.id)
    loader = getLoadersFromInfo(info=info).externalids
    result = await loader.filter_by(inner_id=self.id)
    return result

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    return cls(id=id)

class BaseEternal:
    id: UUID = strawberry.federation.field(external=True)

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    
    # @strawberry.field(description="""All external ids related to the user""")
    # async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
    #     return await resolve_external_ids(self, info)
     
    external_ids = resolve_external_ids
    
    
@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    # @strawberry.field(description="""All external ids related to the group""")
    # async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
    #     return await resolve_external_ids(self, info)
    
    external_ids = resolve_external_ids
    
# @strawberry.federation.type(extend=True, keys=["id"])
# class ProjectGQLModel:

#     id: UUID = strawberry.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: UUID):
#         return None if id is None else ProjectGQLModel(id=id)

#     # @strawberry.field(description="""All external ids related to the project""")
#     # async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
#     #     return await resolve_external_ids(self, info)
    
#     external_ids = resolve_external_ids
    
# @strawberry.federation.type(extend=True, keys=["id"])
# class PublicationGQLModel:

#     id: UUID = strawberry.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: UUID):
#         return None if id is None else PublicationGQLModel(id=id)
    
#     # @strawberry.field(description="""All external ids related to the publication""")
#     # async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
#     #     return await resolve_external_ids(self, info)
    
#     external_ids = resolve_external_ids
    
# @strawberry.federation.type(extend=True, keys=["id"])
# class FacilityGQLModel:

#     id: UUID = strawberry.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: UUID):
#         return None if id is None else FacilityGQLModel(id=id)

#     # @strawberry.field(description="""All external ids related to the facility""")
#     # async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
#     #     return await resolve_external_ids(self, info)
    
#     external_ids = resolve_external_ids