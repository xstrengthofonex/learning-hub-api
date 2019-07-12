import pytest
from asynctest import Mock

from learning_hub.usecases.helpers import IdGenerator


@pytest.fixture
def id_generator():
    return Mock(IdGenerator)
