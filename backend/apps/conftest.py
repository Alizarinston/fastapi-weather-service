import asyncio
import warnings

import pytest
from apps.common.services.testing_client import TestClient
from tortoise import Tortoise


@pytest.fixture(scope='session')
def event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        return loop


@pytest.fixture(scope='function', autouse=True)
async def initialize_database(app):
    from config.orm import TORTOISE_ORM

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        await Tortoise.init(config=TORTOISE_ORM, _create_db=True)

    await Tortoise.generate_schemas()

    yield

    await Tortoise._drop_databases()


@pytest.fixture(scope='session')
def app():
    from apps.app import app as api_app

    return api_app


@pytest.fixture(scope='session')
def client(app):
    return TestClient(app)
