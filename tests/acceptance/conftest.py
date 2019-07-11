import pytest

from learning_hub.app import create_app


@pytest.fixture
def app(loop):
    return loop.run_until_complete(create_app())


@pytest.fixture
def client(loop, app, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))
