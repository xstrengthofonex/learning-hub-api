import pytest
from asynctest import Mock

from learning_hub.auth import JWTAuth
from learning_hub.helpers import IdGenerator


@pytest.fixture
def id_generator():
    return Mock(IdGenerator)


@pytest.fixture
def auth():
    return Mock(JWTAuth)
