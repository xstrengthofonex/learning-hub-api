from uuid import uuid4

import pytest
from asynctest import Mock
from datetime import datetime

from learning_hub.domain.paths import Paths, PathValidator, Path, Assignment
from learning_hub.helpers import Clock, IdGenerator
from learning_hub.usecases.update_path import UpdatePath, UpdatePathRequest, UpdateAssignmentRequest, PathNotFound

TODAY = datetime.now()
USER_ID = str(uuid4())
NEW_ASSIGNMENT_ID = str(uuid4())
ASSIGNMENT_NAME = "Assignment 1"
ASSIGNMENT_RESOURCE = "resource"
ASSIGNMENT_INSTRUCTIONS = "assignment instructions"
ASSIGNMENT_REQUEST = UpdateAssignmentRequest(
    id="",
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS)
PATH_ID = str(uuid4())
TITLE = "title"
DESCRIPTION = "description"
CATEGORIES = ["category"]
UPDATE_PATH_REQUEST = UpdatePathRequest(
    id=PATH_ID,
    title=TITLE,
    author=USER_ID,
    created_on=TODAY,
    updated_on=TODAY,
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
        id=NEW_ASSIGNMENT_ID,
        name=ASSIGNMENT_NAME,
        resource=ASSIGNMENT_RESOURCE,
        instructions=ASSIGNMENT_INSTRUCTIONS)])


@pytest.fixture
def paths():
    return Mock(Paths)


@pytest.fixture
def update_path(paths):
    update_path = UpdatePath(paths)
    update_path.path_validator = Mock(PathValidator)
    update_path.clock = Mock(Clock)
    update_path.id_generator = Mock(IdGenerator)
    update_path.id_generator.generate.side_effect = [NEW_ASSIGNMENT_ID]
    update_path.clock.now.return_value = TODAY
    return update_path


async def test_update_path(update_path):
    result = await update_path.execute(UPDATE_PATH_REQUEST)
    update_path.path_validator.validate.assert_called_with(PATH)
    update_path.paths.add.assert_called_with(PATH)
    assert result.path.assignments[0].id == NEW_ASSIGNMENT_ID


async def test_update_path_returns_no_path_if_path_does_not_exist(update_path):
    with pytest.raises(PathNotFound):
        update_path.paths.find_by_id.return_value = None
        await update_path.execute(UPDATE_PATH_REQUEST)
        update_path.paths.find_by_id.assert_called_with(PATH_ID)
