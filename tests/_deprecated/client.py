import logging
import json

def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    client = TestClient(main.app, raise_server_exceptions=False)
    
    return client

def CreateClientFunction():
    client = createGQLClient()

    async def result(query, variables={}):
        json = {
            "query": query,
            "variables": variables
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variables}")

        response = client.post("/gql", headers=headers, json=json)
        return response.json()
    
    return result

def updateIntrospectionQuery():
    from .introspection import query
    client = createGQLClient()
    inputjson = {"query": query, "variables": {}}
    response = client.post("/gql", headers={}, json=inputjson)

    # Print the raw content of the response
    print(response.content)
    responsejson = None
    # Try to parse the response as JSON
    try:
        responsejson = response.json()
    except json.decoder.JSONDecodeError:
        print(f"Unable to decode JSON response: {response.content}")
        responsejson = None

    # Check if responsejson is not None before accessing it
    if responsejson is not None:
        data = responsejson.get("data", {})
        print(responsejson)
        with open("./introspectionquery.json", "w", encoding="utf-8") as f:
            datastr = json.dumps(data)
            f.write(datastr)
    else:
        print(f"Response is not a valid JSON object. Server response: {response.content}")

updateIntrospectionQuery()
