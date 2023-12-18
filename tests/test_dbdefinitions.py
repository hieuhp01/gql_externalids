import sqlalchemy
import sys
import asyncio

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_externalids.DBDefinitions import BaseModel
from gql_externalids.DBDefinitions import ExternalIdTypeModel, ExternalIdModel, ExternalIdCategoryModel

from .shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_load_demo_data():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    #data = get_demodata()


from gql_externalids.DBDefinitions import ComposeConnectionString


def test_connection_string():
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    #assert "@" in connectionString



from gql_externalids.DBDefinitions import startEngine


@pytest.mark.asyncio
async def test_table_start_engine():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
 
from gql_externalids.utils.DBFeeder import initDB


@pytest.mark.asyncio
async def test_initDB():
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
    await initDB(async_session_maker)   
