import pytest
from GraphTypeDefinitions import schema

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_externalid_category = createResolveReferenceTest(tableName="externalidcategories", gqltype="ExternalIdCategoryGQLModel", attributeNames=["id", "name", "lastchange"])

test_query_externalid_category_page = createPageTest(tableName="externalidcategories", queryEndpoint="externalidcategoryPage")

test_insert_externalid_category = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $nameEn: String!) {
        result: externalidcategoryInsert(externalidcategory: {id: $id, name: $name, nameEn: $nameEn}) {
            id
            msg
            externalidcategory {
                id
                name
            }
        }
    }""",
    variables={"id": "fc7f95b5-410c-4a26-a4e9-6b0b2a841645", "name": "new name", "nameEn": "new name en"},
)

test_update_externalid_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $nameEn: String!, $lastchange: DateTime!) {
        result: externalidcategoryUpdate(externalidcategory: {id: $id, name: $name, nameEn: $nameEn, lastchange: $lastchange}) {
            id
            msg
            externalidcategory {
                id
                name
            }
        }
    }""",
    variables={"id": "0ee3a92d-971f-499a-956f-ca6edb8d6094", "name": "new name", "nameEn": "new name en"},
    tableName="externalidcategories"
)