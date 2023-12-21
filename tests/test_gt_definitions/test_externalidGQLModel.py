import pytest
from gql_externalids.GraphTypeDefinitions import schema
import logging

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
    CreateSchemaFunction
)
from tests.client import CreateClientFunction

from tests.gqlshared import (
    append,
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_externalid = createResolveReferenceTest(tableName="externalids", gqltype="ExternalIdGQLModel", attributeNames=["id", "name", "lastchange", "nameEn", "innerId","outerId","idType {id}","typeName"])

def createInternalIDTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        
        def testResult(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None
            
            respdata = resp.get("data", None)
            assert respdata is not None
            
            respdata = respdata[queryEndpoint]
            assert respdata is not None

        schemaExecutor = CreateSchemaFunction()
        clientExecutor = CreateClientFunction()

        data = get_demodata()
        datarow = data[tableName][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = f"query($typeidId: UUID!, $outerId: String!){{ {queryEndpoint}(typeidId: $typeidId, outerId: $outerId) }}"

        variable_values = {"typeidId": f'{datarow["typeid_id"]}', "outerId": f'{datarow["outer_id"]}'}
        
        append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
        logging.debug(f"query for {query} with {variable_values}")

        resp = await schemaExecutor(query, variable_values)
        testResult(resp)
        resp = await clientExecutor(query, variable_values)
        testResult(resp)

    return result_test

def createExternalIDTest(tableName, queryEndpoint, attributeNames=["id", "innerId", "outerId"]):
    @pytest.mark.asyncio
    async def result_test():
        
        def testResult(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None
            
            respdata = resp.get("data", None)
            assert respdata is not None
            
            respdata = respdata[queryEndpoint]
            assert respdata is not None

        schemaExecutor = CreateSchemaFunction()
        clientExecutor = CreateClientFunction()

        data = get_demodata()
        datarow = data[tableName][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = f"query($typeidId: UUID!, $innerId: UUID!){{ {queryEndpoint}(typeidId: $typeidId, innerId: $innerId) {content} }}"

        variable_values = {"typeidId": f'{datarow["typeid_id"]}', "innerId": f'{datarow["inner_id"]}'}
        
        append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
        logging.debug(f"query for {query} with {variable_values}")

        resp = await schemaExecutor(query, variable_values)
        testResult(resp)
        resp = await clientExecutor(query, variable_values)
        testResult(resp)

    return result_test

test_query_internalid_byexternalid = createInternalIDTest(tableName="externalids", queryEndpoint="internalId")
test_query_externalid_byinternalid = createExternalIDTest(tableName="externalids", queryEndpoint="externalIds")

