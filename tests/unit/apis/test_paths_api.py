import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.paths_api import PathsAPI
from learning_hub.domain.participations import Participations
from learning_hub.domain.paths import Paths
from learning_hub.domain.users import Users, User
from learning_hub.usecases.create_path import *
from tests.unit.apis.builders import CreatePathRequestBuilder, CreateAssignmentRequestBuilder
from tests.unit.apis.conftest import create_mock_request
from tests.unit.builders import PathBuilder, ParticipationBuilder, AssignmentBuilder


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


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def paths():
    return Mock(Paths)


@pytest.fixture
def participations():
    return Mock(Participations)


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


async def test_get_path_returns_path_with_id(paths, participations):
    paths.find_by_id.return_value = PATH
    participations.find_participations_for_path_id.return_value = [PARTICIPATION]
    mock_request = create_mock_request()
    mock_request.app.get.side_effect = [paths, participations]
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
    assert result.get("participants") == 1
    assert result.get("created_on") == PATH.created_on.timestamp()
    assert result.get("updated_on") == PATH.updated_on.timestamp()
    assert result.get("categories") == PATH.categories
    assert result.get("assignments") == [
        dict(id=assignment.id, name=assignment.name,
             resource=assignment.resource, instructions=assignment.instructions)]


async def test_get_path_returns_404_if_path_not_found(paths, participations):
    paths.find_by_id.return_value = None
    participations.find_participations_for_path_id.return_value = None
    mock_request = create_mock_request()
    mock_request.app.get.side_effect = [paths, participations]
    mock_request.match_info.get.return_value = PATH_ID
    paths_api = PathsAPI()

    response = await paths_api.get_path(mock_request)

    paths.find_by_id.assert_called_with(PATH_ID)
    assert response.status == 404
    assert response.content_type == "application/json"
    result = json.loads(response.text)
    assert result.get("message") == "Learning path not found"
