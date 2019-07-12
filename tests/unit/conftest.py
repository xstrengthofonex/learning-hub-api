import pytest
from asynctest import Mock

from learning_hub.auth import JWTAuth
from learning_hub.usecases.helpers import IdGenerator
from tests.unit.apis.test_users_api import TOKEN


@pytest.fixture
def id_generator():
    return Mock(IdGenerator)


@pytest.fixture
def auth():
    auth = Mock(JWTAuth)
    auth.generate_token.return_value = TOKEN
    return auth