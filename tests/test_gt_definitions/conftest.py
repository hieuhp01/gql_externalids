import logging
import datetime
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def GQLInsertQueries():
    result = {
        "externalids": {
            "create": """
mutation ($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!) {
    externalidInsert(
        externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id}
    ) {
        id
        msg
    }
}""",
            "read": """query($id: UUID!){ result: externalidById(id: $id) { id }}""",
},
        "externalidtypes": {
            "create": """
mutation ($id: UUID!, $name: String!, $nameEn: String!) {
    externaltypeidInsert(
        externaltypeid: {id: $id, name: $name, nameEn: $nameEn}
    ) {
        id
        msg
    }
}""",
            "read": """query($id: UUID!){ result: externalidtypeById(id: $id) { id }}""",
},
        "externalidcategories": {
            "create": """
mutation ($id: UUID!, $name: String!, $nameEn: String!) {
    externalidcategoryInsert(
        externalidcategory: {id: $id, name: $name, nameEn: $nameEn}
    ) {
        id
        msg
    }
}""",
            "read": """query($id: UUID!){ result: externalidcategoryById(id: $id) { id }}""",
},
 
    }
    
    return result


@pytest_asyncio.fixture
async def FillDataViaGQL(DemoData, GQLInsertQueries, ClientExecutorAdmin):
    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for tablename, queryset in GQLInsertQueries.items():
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            if readResponse["data"]["result"] is None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
        logging.info(f"{tablename} initialized via gql query")
    logging.info(f"All WANTED tables are initialized")