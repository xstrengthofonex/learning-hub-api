import json
from uuid import uuid4

import pytest
from aiohttp import web
from asynctest import Mock

from learning_hub.apis.users_api import UsersAPI
from learning_hub.usecases.create_user import *

CREATE_USER_REQUEST = CreateUserRequest(
    email="example@email.com",
    username="username",
    password="password")
USER_ID = str(uuid4())
TOKEN = "xxxxx.yyyyy.zzzzz"
SECRET = "Secret"


@pytest.fixture
def create_user():
    create_user = Mock(CreateUser)
    create_user.execute.return_value = CreateUserResponse(USER_ID)
    return create_user


@pytest.fixture
def mock_request(create_user, auth):
    mock_request = Mock(web.Request)
    mock_request.json.return_value = dict(
        email=CREATE_USER_REQUEST.email,
        username=CREATE_USER_REQUEST.username,
        password=CREATE_USER_REQUEST.password)
    mock_request.app.get.side_effect = [create_user, auth]
    return mock_request


async def test_register_user_should_create_user(mock_request, create_user, auth):
    users_api = UsersAPI()
    await users_api.register_user(mock_request)
    create_user.execute.assert_called_with(CREATE_USER_REQUEST)


async def test_register_user_should_return_user_id_and_generated_token(mock_request, create_user, auth):
    users_api = UsersAPI()
    response = await users_api.register_user(mock_request)
    create_user.execute.assert_called_with(CREATE_USER_REQUEST)
    auth.generate_token.assert_called_with(USER_ID)
    assert response.status == 201
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(userId=USER_ID, token=TOKEN)


async def test_register_user_should_return_400_if_request_data_is_invalid(mock_request, create_user, auth):
    message = "Some Error"
    users_api = UsersAPI()
    create_user.execute.side_effect = ValueError(message)
    response = await users_api.register_user(mock_request)
    assert response.status == 400
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(errors=[message])
