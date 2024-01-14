import pytest
# from gql_externalids.GraphTypeDefinitions import schema

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_externalid_type = createResolveReferenceTest(tableName="externalidtypes", gqltype="ExternalIdTypeGQLModel", attributeNames=["id", "name", "lastchange"])

test_query_externalid_type_page = createPageTest(tableName="externalidtypes", queryEndpoint="externalidtypePage")
test_query_externalid_type_byid = createByIdTest(tableName="externalidtypes", queryEndpoint="externalidtypeById")


test_insert_externalid_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $nameEn: String!) {
        result: externaltypeidInsert(externaltypeid: {id: $id, name: $name, nameEn: $nameEn}) {
            id
            msg
            externaltypeid {
                id
                name
                category { id }
            }
        }
    }""",
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name", "nameEn": "new name en"}
)

test_update_externalid_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!, $nameEn: String!) {
        result: externaltypeidUpdate(externaltypeid: {id: $id, name: $name, lastchange: $lastchange, nameEn: $nameEn}) {
            id
            msg
            externaltypeid {
                id
                name
            }
        }
    }""",
    variables={"id": "53697b35-9f67-41e5-abed-04d7d4865cf2", "name": "new name", "nameEn": "new name en"},
    tableName="externalidtypes"
)