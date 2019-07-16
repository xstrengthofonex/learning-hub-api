from uuid import uuid4

import pytest
from asynctest import Mock
from datetime import datetime

from learning_hub.domain.paths import Paths
from learning_hub.usecases.create_path import *
from learning_hub.helpers import IdGenerator, Clock

USER_ID = str(uuid4())
ASSIGNMENT_ID = str(uuid4())
ASSIGNMENT_NAME = "Assignment 1"
ASSIGNMENT_RESOURCE = "resource"
ASSIGNMENT_INSTRUCTIONS = "assignment instructions"
ASSIGNMENT_REQUEST = CreateAssignmentRequest(
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS)
PATH_ID = str(uuid4())
TITLE = "title"
DESCRIPTION = "description"
CATEGORIES = ["category"]
TODAY = datetime.now()
CREATE_PATH_REQUEST = CreatePathRequest(
    title=TITLE,
    author=USER_ID,
    description=DESCRIPTION,
    categories=CATEGORIES,
    assignments=[ASSIGNMENT_REQUEST])
PATH = Path(
    id=PATH_ID,
    title=TITLE,
    author=USER_ID,
    created_on=TODAY,
    updated_on=TODAY,
    description=DESCRIPTION,
    categories=CATEGORIES,
    assignments=[Assignment(
        id=ASSIGNMENT_ID,
        name=ASSIGNMENT_NAME,
        resource=ASSIGNMENT_RESOURCE,
        instructions=ASSIGNMENT_INSTRUCTIONS)])


@pytest.fixture
def paths():
    return Mock(Paths)


@pytest.fixture
def create_path(paths):
    create_path = CreatePath(paths)
    create_path.path_validator = Mock(PathValidator)
    create_path.clock = Mock(Clock)
    create_path.id_generator = Mock(IdGenerator)
    create_path.id_generator.generate.side_effect = [PATH_ID, ASSIGNMENT_ID]
    create_path.clock.now.return_value = TODAY
    return create_path


async def test_create_a_new_user(create_path, paths):
    result = await create_path.execute(CREATE_PATH_REQUEST)
    paths.add.assert_called_with(PATH)
    assert result.path_id == PATH_ID


async def test_invalid_path_returns_value_error(create_path):
    create_path.path_validator.validate.side_effect = ValueError()
    with pytest.raises(ValueError):
        await create_path.execute(CREATE_PATH_REQUEST)
