import strawberry
from typing import List

from .externalIdGQLModel import ExternalIdGQLModel

def getLoaders(info):
    return info.context["all"]

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
async def resolve_external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
    loader = getLoaders(info=info).externalids_inner_id
    result = await loader.load(self.id)
    return result

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        if id is None:
            return None
        return UserGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the user""")
    async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
        return await resolve_external_ids(self, info)


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return GroupGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the group""")
    async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
        return await resolve_external_ids(self, info)
    
@strawberry.federation.type(extend=True, keys=["id"])
class ProjectGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return ProjectGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the project""")
    async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
        return await resolve_external_ids(self, info)
    
@strawberry.federation.type(extend=True, keys=["id"])
class PublicationGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return PublicationGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the publication""")
    async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
        return await resolve_external_ids(self, info)
    
@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return FacilityGQLModel(id=id)

    @strawberry.field(description="""All external ids related to the facility""")
    async def external_ids(self, info: strawberry.types.Info) -> List[ExternalIdGQLModel]:
        return await resolve_external_ids(self, info)