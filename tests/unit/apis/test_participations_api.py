import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.participations_api import ParticipationsAPI
from learning_hub.usecases.create_participation import *
from tests.unit.apis.conftest import create_mock_request

PATH_ID = str(uuid4())
USER_ID = str(uuid4())
PARTICIPATION_ID = str(uuid4())
CREATE_PARTICIPATION_REQUEST = CreateParticipationRequest(
    path_id=PATH_ID,
    user_id=USER_ID)
CREATE_PARTICIPATION_RESPONSE = CreateParticipationResponse(
    participation_id=PARTICIPATION_ID)


@pytest.fixture
def usecase():
    create_participation = Mock(CreateParticipation)
    create_participation.execute.return_value = CREATE_PARTICIPATION_RESPONSE
    return create_participation


@pytest.fixture
def api():
    return ParticipationsAPI()


@pytest.fixture
def create_participation_http_request(usecase):
    request = create_mock_request(dict(pathId=PATH_ID))
    request.get.return_value = USER_ID
    request.app.get.side_effect = [usecase]
    return request


async def test_create_participation_creates_new_participation(
        usecase, api, create_participation_http_request):
    response = await api.create_participation(create_participation_http_request)

    usecase.execute.assert_called_with(CREATE_PARTICIPATION_REQUEST)
    assert response.status == 201
    assert json.loads(response.text) == dict(participationId=PARTICIPATION_ID)


async def test_create_participation_returns_404_error_for_path_not_found(
        usecase, api, create_participation_http_request):
    usecase.execute.side_effect = PathNotFound
    response = await api.create_participation(create_participation_http_request)

    usecase.execute.assert_called_with(CREATE_PARTICIPATION_REQUEST)
    assert response.status == 404
