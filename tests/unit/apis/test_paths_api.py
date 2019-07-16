import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.paths_api import PathsAPI
from learning_hub.domain.users import Users, User
from learning_hub.usecases.create_path import *
from tests.unit.apis.conftest import create_mock_request


USER_ID = str(uuid4())
USER = User(id=USER_ID, email="email", password="password", username="username")
TOKEN = "xxxxx.yyyyy.zzzzz"
TITLE = "title"
DESCRIPTION = "description"
CATEGORIES = ["Category"]
ASSIGNMENT_NAME = "Assignment 1"
ASSIGNMENT_RESOURCE = "http://resource.com"
ASSIGNMENT_INSTRUCTIONS = "So instructions"
ASSIGNMENTS = [dict(
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS)]
CREATE_PATH_REQUEST_DATA = dict(
    token=TOKEN,
    title=TITLE,
    description=DESCRIPTION,
    categories=CATEGORIES,
    assignments=ASSIGNMENTS)
ASSIGNMENT_REQUEST = CreateAssignmentRequest(
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS)
CREATE_PATH_REQUEST = CreatePathRequest(
    title=TITLE,
    author=USER_ID,
    description=DESCRIPTION,
    categories=CATEGORIES,
    assignments=[ASSIGNMENT_REQUEST])
PATH_ID = str(uuid4())


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def create_path():
    return Mock(CreatePath)


@pytest.fixture(autouse=True)
def setup(auth):
    auth.generate_token.return_value = TOKEN


async def test_creates_path(create_path, auth, users):
    mock_request = create_mock_request(CREATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = USER_ID
    mock_request.app.get.side_effect = [create_path]
    create_path.execute.return_value = CreatePathResponse(path_id=PATH_ID)
    paths_api = PathsAPI()

    response = await paths_api.create_path(mock_request)

    mock_request.get.assert_called_with("user_id")
    create_path.execute.assert_called_with(CREATE_PATH_REQUEST)
    assert response.status == 201
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(pathId=PATH_ID)


async def test_create_path_raises_400_if_request_data_is_invalid(create_path, auth, users):
    message = "Some Error"
    create_path.execute.side_effect = ValueError((message,))
    mock_request = create_mock_request(CREATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = USER_ID
    mock_request.app.get.side_effect = [create_path]
    create_path.execute.return_value = CreatePathResponse(path_id=PATH_ID)
    paths_api = PathsAPI()

    response = await paths_api.create_path(mock_request)

    assert response.status == 400
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(errors=[message])
