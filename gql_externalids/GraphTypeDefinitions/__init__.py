from typing import List, Union
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager



###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################


# from gql_forms.GraphResolvers import resolveRequestsByThreeLetters

from .externalIdCategoryGQLModel import ExternalIdCategoryGQLModel
from .externalIdTypeGQLModel import ExternalIdTypeGQLModel
from .externalIdGQLModel import ExternalIdGQLModel

from .externals import UserGQLModel, GroupGQLModel

from gql_externalids.utils.Dataloaders import getUserFromInfo

@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(description="""Say hello to the world""")
    async def say_hello_forms(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        user = getUserFromInfo(info)
        result = f"Hello {id} `{user}`"
        return result

    from .externalIdGQLModel import external_ids
    external_ids = external_ids

    from .externalIdGQLModel import internal_id
    internal_id = internal_id

    from .externalIdTypeGQLModel import externalid_type_page
    externalidtype_page = externalid_type_page

    from .externalIdTypeGQLModel import externalidtype_by_id
    externalidtype_by_id = externalidtype_by_id

    from .externalIdCategoryGQLModel import externalid_category_page
    externalidcategory_page = externalid_category_page
    


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

   
@strawberry.type(description="""Type for mutation root""")
class Mutation:

    from .externalIdGQLModel import externalid_insert
    externalid_insert = externalid_insert

    from .externalIdGQLModel import externalid_delete
    externalid_delete = externalid_delete
    
    from .externalIdGQLModel import externalid_update
    externalid_update = externalid_update

    from.externalIdTypeGQLModel import externaltypeid_insert
    externaltypeid_insert = externaltypeid_insert

    from.externalIdTypeGQLModel import externaltypeid_update
    externaltypeid_update = externaltypeid_update
    
    from .externalIdCategoryGQLModel import externalidcategory_insert
    externalidcategory_insert = externalidcategory_insert

    from .externalIdCategoryGQLModel import externalidcategory_update
    externalidcategory_update = externalidcategory_update

    

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, types=(UserGQLModel, GroupGQLModel ), mutation=Mutation)