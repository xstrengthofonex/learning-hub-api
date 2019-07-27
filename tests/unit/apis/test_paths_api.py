import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.paths_api import PathsAPI
from learning_hub.domain.paths import Paths
from learning_hub.domain.users import Users, User
from learning_hub.usecases.create_path import *
from learning_hub.usecases.update_path import *
from tests.unit.apis.builders import CreatePathRequestBuilder, CreateAssignmentRequestBuilder
from tests.unit.apis.conftest import create_mock_request
from tests.unit.builders import PathBuilder, ParticipationBuilder, AssignmentBuilder

TODAY = datetime.now()
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
PATH = PathBuilder(id=PATH_ID, author=USER_ID, assignments=[
    AssignmentBuilder()]).build()
PARTICIPATION = ParticipationBuilder(path_id=PATH_ID, user_id=USER_ID).build()


UPDATE_PATH = PathBuilder(
    author=USER_ID,
    created_on=TODAY,
    updated_on=TODAY,
    assignments=[
        AssignmentBuilder(id=str(uuid4()), name="Assignment 1", resource="http://resource1", instructions=""),
        AssignmentBuilder(id="", name="Assignment 2", resource="http://resource2", instructions="")
    ]).build()
UPDATE_PATH_REQUEST = UpdatePathRequest(
    id=UPDATE_PATH.id,
    title=UPDATE_PATH.title,
    author=UPDATE_PATH.author,
    created_on=UPDATE_PATH.created_on,
    updated_on=UPDATE_PATH.updated_on,
    description=UPDATE_PATH.description,
    categories=UPDATE_PATH.categories,
    assignments=[UpdateAssignmentRequest(
        id=a.id, resource=a.resource, name=a.name, instructions=a.instructions)
        for a in UPDATE_PATH.assignments])
UPDATE_PATH_REQUEST_DATA = dict(
    id=UPDATE_PATH_REQUEST.id,
    title=UPDATE_PATH_REQUEST.title,
    author=UPDATE_PATH_REQUEST.author,
    description=UPDATE_PATH_REQUEST.description,
    categories=UPDATE_PATH_REQUEST.categories,
    created_on=UPDATE_PATH_REQUEST.created_on.timestamp(),
    updated_on=UPDATE_PATH_REQUEST.updated_on.timestamp(),
    assignments=[dict(
        id=a.id,
        name=a.name,
        resource=a.resource,
        instructions=a.instructions) for a in UPDATE_PATH_REQUEST.assignments])
UPDATE_PATH_RESPONSE = UpdatePathResponse(path=UPDATE_PATH)


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def paths():
    return Mock(Paths)


@pytest.fixture
def create_path():
    return Mock(CreatePath)


@pytest.fixture
def update_path():
    return Mock(UpdatePath)


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


async def test_get_path_returns_path_with_id(paths):
    paths.find_by_id.return_value = PATH
    mock_request = create_mock_request()
    mock_request.app.get.side_effect = [paths]
    mock_request.match_info.get.return_value = PATH_ID
    paths_api = PathsAPI()

    response = await paths_api.get_path(mock_request)

    paths.find_by_id.assert_called_with(PATH_ID)
    assert response.status == 200
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assignment = PATH.assignments[0]
    assert result.get("id") == PATH.id
    assert result.get("title") == PATH.title
    assert result.get("created_on") == PATH.created_on.timestamp()
    assert result.get("updated_on") == PATH.updated_on.timestamp()
    assert result.get("categories") == PATH.categories
    assert result.get("assignments") == [
        dict(id=assignment.id, name=assignment.name,
             resource=assignment.resource, instructions=assignment.instructions)]


async def test_get_path_returns_404_if_path_not_found(paths):
    paths.find_by_id.return_value = None
    mock_request = create_mock_request()
    mock_request.app.get.side_effect = [paths]
    mock_request.match_info.get.return_value = PATH_ID
    paths_api = PathsAPI()

    response = await paths_api.get_path(mock_request)

    paths.find_by_id.assert_called_with(PATH_ID)
    assert response.status == 404
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert result.get("message") == "Learning path not found"


async def test_updates_existing_path(update_path):
    update_path.execute.return_value = UPDATE_PATH_RESPONSE
    mock_request = create_mock_request(UPDATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = USER_ID
    mock_request.app.get.side_effect = [update_path]
    paths_api = PathsAPI()

    response = await paths_api.update_path(mock_request)

    mock_request.app.get.assert_called_with("update_path")
    update_path.execute.assert_called_with(UPDATE_PATH_REQUEST)
    assert response.status == 200
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert result.get("id") == UPDATE_PATH.id
    assert result.get("title") == UPDATE_PATH.title
    assert result.get("created_on") == UPDATE_PATH.created_on.timestamp()
    assert result.get("updated_on") == UPDATE_PATH.updated_on.timestamp()
    assert result.get("categories") == UPDATE_PATH.categories


async def test_update_path_returns_403_if_user_id_does_not_match_author(update_path):
    update_path.execute.return_value = UPDATE_PATH_RESPONSE
    mock_request = create_mock_request(UPDATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = "DifferentUser"
    mock_request.app.get.side_effect = [update_path]
    paths_api = PathsAPI()

    response = await paths_api.update_path(mock_request)

    mock_request.app.get.assert_called_with("update_path")
    assert response.status == 403
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert result.get("message") == "Update Request Forbidden"


async def test_update_path_returns_404_if_path_does_not_exist(update_path):
    update_path.execute.side_effect = PathNotFound
    mock_request = create_mock_request(UPDATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = USER_ID
    mock_request.app.get.side_effect = [update_path]
    paths_api = PathsAPI()

    response = await paths_api.update_path(mock_request)

    mock_request.app.get.assert_called_with("update_path")
    assert response.status == 404
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert result.get("message") == "Learning path not found"


async def test_update_path_returns_400_if_validation_error_is_raised(update_path):
    error_message = "Some Error"
    update_path.execute.side_effect = ValueError([error_message])
    mock_request = create_mock_request(UPDATE_PATH_REQUEST_DATA)
    mock_request.get.return_value = USER_ID
    mock_request.app.get.side_effect = [update_path]
    paths_api = PathsAPI()

    response = await paths_api.update_path(mock_request)

    mock_request.app.get.assert_called_with("update_path")
    assert response.status == 400
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert error_message in result.get("errors")
