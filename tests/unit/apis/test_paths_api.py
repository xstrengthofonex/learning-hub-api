import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.paths_api import PathsAPI
from learning_hub.domain.users import Users, User
from learning_hub.usecases.create_path import *
from tests.unit.apis.builders import CreatePathRequestBuilder, CreateAssignmentRequestBuilder
from tests.unit.apis.conftest import create_mock_request


USER_ID = str(uuid4())
USER = User(id=USER_ID, email="email", password="password", username="username")
TOKEN = "xxxxx.yyyyy.zzzzz"
CREATE_PATH_REQUEST = CreatePathRequestBuilder(
    author=USER_ID,
    assignments=[CreateAssignmentRequestBuilder().build()],
    categories=["Categories"]).build()
CREATE_PATH_REQUEST_DATA = dict(
    token=TOKEN,
    title=CREATE_PATH_REQUEST.title,
    description=CREATE_PATH_REQUEST.description,
    categories=CREATE_PATH_REQUEST.categories,
    assignments=[dict(
        name=a.name, resource=a.resource, instructions=a.instructions
    ) for a in CREATE_PATH_REQUEST.assignments])
PATH_ID = str(uuid4())


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def create_path():
    return Mock(CreatePath)


async def test_creates_path(create_path, users):
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


async def test_create_path_raises_400_if_request_data_is_invalid(create_path, users):
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
