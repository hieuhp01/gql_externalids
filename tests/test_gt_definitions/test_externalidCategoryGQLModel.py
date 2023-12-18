import pytest
from gql_externalids.GraphTypeDefinitions import schema

from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_externalid_category = createResolveReferenceTest(tableName="externalidcategories", gqltype="ExternalIdCategoryGQLModel", attributeNames=["id", "name", "lastchange"])

test_query_externalid_category_page = createPageTest(tableName="externalidcategories", queryEndpoint="externalidcategoryPage")
