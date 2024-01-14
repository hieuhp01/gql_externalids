import pytest
# from gql_externalids.GraphTypeDefinitions import schema
import logging
# import sqlalchemy
# import uuid

# from tests._deprecated.shared import (
#     prepare_demodata,
#     prepare_in_memory_sqllite,
#     get_demodata,
#     createContext,
#     CreateSchemaFunction
# )
# from tests._deprecated.client import CreateClientFunction

from .gt_utils import ( 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

# test_reference_externalid = createResolveReferenceTest(tableName="externalids", gqltype="ExternalIdGQLModel", attributeNames=["id", "name", "lastchange", "nameEn", "innerId","outerId","idType {id}","typeName"])
test_reference_externalid = createResolveReferenceTest(tableName="externalids", gqltype="ExternalIdGQLModel", attributeNames=["id"])

# def createInternalIDTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
#     @pytest.mark.asyncio
#     async def result_test():
        
#         def testResult(resp):
#             print("response", resp)
#             errors = resp.get("errors", None)
#             assert errors is None
            
#             respdata = resp.get("data", None)
#             assert respdata is not None
            
#             respdata = respdata[queryEndpoint]
#             assert respdata is not None

#         schemaExecutor = CreateSchemaFunction()
#         clientExecutor = CreateClientFunction()

#         data = get_demodata()
#         datarow = data[tableName][0]
#         content = "{" + ", ".join(attributeNames) + "}"
#         query = f"query($typeidId: UUID!, $outerId: String!){{ {queryEndpoint}(typeidId: $typeidId, outerId: $outerId) {content}  }}"

#         variable_values = {"typeidId": f'{datarow["typeid_id"]}', "outerId": f'{datarow["outer_id"]}'}
        
#         append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
#         logging.debug(f"query for {query} with {variable_values}")

#         resp = await schemaExecutor(query, variable_values)
#         testResult(resp)
#         resp = await clientExecutor(query, variable_values)
#         testResult(resp)

#     return result_test

# def createExternalIDTest(tableName, queryEndpoint, attributeNames=["id", "innerId", "outerId"]):
#     @pytest.mark.asyncio
#     async def result_test():
        
#         def testResult(resp):
#             print("response", resp)
#             errors = resp.get("errors", None)
#             assert errors is None
            
#             respdata = resp.get("data", None)
#             assert respdata is not None
            
#             respdata = respdata[queryEndpoint]
#             assert respdata is not None

#         schemaExecutor = CreateSchemaFunction()
#         clientExecutor = CreateClientFunction()

#         data = get_demodata()
#         datarow = data[tableName][0]
#         content = "{" + ", ".join(attributeNames) + "}"
#         query = f"query($typeidId: UUID!, $innerId: UUID!){{ {queryEndpoint}(typeidId: $typeidId, innerId: $innerId) {content} }}"

#         variable_values = {"typeidId": f'{datarow["typeid_id"]}', "innerId": f'{datarow["inner_id"]}'}
        
#         append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
#         logging.debug(f"query for {query} with {variable_values}")

#         resp = await schemaExecutor(query, variable_values)
#         testResult(resp)
#         resp = await clientExecutor(query, variable_values)
#         testResult(resp)

#     return result_test

# def createUpdateQuery(query="{}", variables={}, tableName=""):
#     @pytest.mark.asyncio
#     async def test_update():
#         logging.debug("test_update")
#         assert variables.get("inner_id", None) is not None, "variables has not id"
#         variables["inner_id"] = uuid.UUID(f"{variables['inner_id']}")
#         assert "$lastchange: DateTime!" in query, "query must have parameter $lastchange: DateTime!"
#         assert "lastchange: $lastchange" in query, "query must use lastchange: $lastchange"
#         assert tableName != "", "missing table name"

#         async_session_maker = await prepare_in_memory_sqllite()
#         await prepare_demodata(async_session_maker)

#         print("variables['inner_id']", variables, flush=True)
#         statement = sqlalchemy.text(f"SELECT inner_id, lastchange FROM {tableName} WHERE inner_id=:inner_id").bindparams(inner_id=variables['inner_id'])
#         #statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
#         print("statement", statement, flush=True)
#         async with async_session_maker() as session:
#             rows = await session.execute(statement)
#             row = rows.first()
    
#             print("row", row)
#             id = row[0]
#             lastchange = row[1]

#             print(id, lastchange)

#         variables["lastchange"] = lastchange
#         variables["inner_id"] = f'{variables["inner_id"]}'
#         context_value = createContext(async_session_maker)
#         logging.debug(f"query for {query} with {variables}")
#         print(f"query for {query} with {variables}")

#         append(queryname=f"query_{tableName}", mutation=query, variables=variables)

#         resp = await schema.execute(
#             query=query, 
#             variable_values=variables, 
#             context_value=context_value
#         )

#         assert resp.errors is None
#         respdata = resp.data
#         assert respdata is not None
#         print("respdata", respdata)
#         keys = list(respdata.keys())
#         assert len(keys) == 1, "expected update test has one result"
#         key = keys[0]
#         result = respdata.get(key, None)
#         assert result is not None, f"{key} is None (test update) with {query}"
#         entity = None
#         for key, value in result.items():
#             print(key, value, type(value))
#             if isinstance(value, dict):
#                 entity = value
#                 break

#         if entity is not None:
#             for key, value in entity.items():
#                 if key in ["inner_id", "lastchange"]:
#                     continue
#                 print("attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}")
#                 assert value == variables[key], f"test on update failed {value} != {variables[key]}"
#         else:
#             print("No entity returned by the mutation.")
            

        

#     return test_update

# def createDeleteQuery(query="{}", variables={}, tableName=""):
#     @pytest.mark.asyncio
#     async def test_delete():
#         logging.debug("test_delete")
#         assert variables.get("inner_id", None) is not None, "variables has not id"
#         variables["inner_id"] = str(uuid.UUID(f"{variables['inner_id']}"))

#         async_session_maker = await prepare_in_memory_sqllite()
#         await prepare_demodata(async_session_maker)
        
#         print(f"inner_id: {variables['inner_id']}")
#         print(f"tableName: {tableName}")

#         statement = sqlalchemy.text(f"SELECT inner_id FROM {tableName} WHERE inner_id=:inner_id").bindparams(inner_id=variables['inner_id'])
#         async with async_session_maker() as session:
#             rows = await session.execute(statement)
#             row = rows.first()
#             assert row is None, "Row does not exist"

#         context_value = createContext(async_session_maker)
#         logging.debug(f"query for {query} with {variables}")

#         append(queryname=f"query_{tableName}", mutation=query, variables=variables)

#         resp = await schema.execute(
#             query=query, 
#             variable_values=variables, 
#             context_value=context_value
#         )

#         assert resp.errors is None
#         respdata = resp.data
#         assert respdata is not None
#         keys = list(respdata.keys())
#         assert len(keys) == 1, "expected delete test has one result"
#         key = keys[0]
#         result = respdata.get(key, None)
#         assert result is not None, f"{key} is None (test delete) with {query}"
#         assert result['msg'] == 'ok', "Delete operation failed"

#         # Check if the row has been deleted
#         async with async_session_maker() as session:
#             rows = await session.execute(statement)
#             row = rows.first()
#             assert row is None, "Row still exists after delete"

#     return test_delete

# test_query_internalid_byexternalid = createInternalIDTest(tableName="externalids", queryEndpoint="internalId")
# test_query_externalid_byinternalid = createExternalIDTest(tableName="externalids", queryEndpoint="externalIds")

test_externalid_insert = createFrontendQuery(query="""
    mutation($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!) { 
        result: externalidInsert(externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id}) { 
            id
            msg
            externalid {
                id
                outerId 
                
                idType { id }
                lastchange
                created
                changedby { id }
                               
            }
        }
    }
    """, 
    variables={"inner_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "typeid_id": "0c37b3e1-a937-4776-9543-37ae846411de", "outer_id": "777"},
)

# test_externalid_update = createUpdateQuery(
#     query="""
#         mutation($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!, $lastchange: DateTime!) {
#             externalidUpdate(externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id, lastchange: $lastchange}) {
#                 id
#                 msg
#                 externalid {
#                     id
#                     outerId
                    
#                     idType { id }
#                     lastchange
#                 }
#             }
#         }
#     """,
#     variables={"inner_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "typeid_id": "53697b35-9f67-41e5-abed-04d7d4865cf2", "outer_id": "777" },
#     tableName="externalids"
# )

# test_externalid_delete = createDeleteQuery(
#     query="""
#         mutation($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!) {
#             externalidDelete(externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id}) {
#                 id
#                 msg
#             }
#         }
#     """,
#     variables={"inner_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "typeid_id": "d00ec0b6-f27c-497b-8fc8-ddb4e2460717", "outer_id": "666"},
#     tableName="externalids"
# )
