import json
from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.apis.users_api import UsersAPI
from learning_hub.usecases.create_user import *
from tests.unit.apis.builders import CreateUserRequestBuilder
from tests.unit.apis.conftest import create_mock_request

CREATE_USER_REQUEST = CreateUserRequestBuilder().build()
USER_ID = str(uuid4())
USER = User(
    id=USER_ID,
    email=CreateUserRequest.email,
    username=CREATE_USER_REQUEST.username,
    password=CREATE_USER_REQUEST.password)
TOKEN = "xxxxx.yyyyy.zzzzz"
SECRET = "Secret"


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def create_user():
    create_user = Mock(CreateUser)
    create_user.execute.return_value = CreateUserResponse(USER_ID)
    return create_user


@pytest.fixture(autouse=True)
def setup(auth):
    auth.generate_token.return_value = TOKEN


async def test_register_user_should_create_user(create_user, auth):
    mock_request = create_mock_request(data=dict(
        email=CREATE_USER_REQUEST.email,
        username=CREATE_USER_REQUEST.username,
        password=CREATE_USER_REQUEST.password))
    mock_request.app.get.side_effect = [create_user, auth]
    users_api = UsersAPI()
    await users_api.register_user(mock_request)
    create_user.execute.assert_called_with(CREATE_USER_REQUEST)


async def test_register_user_should_return_user_id_and_generated_token(create_user, auth):
    mock_request = create_mock_request(data=dict(
        email=CREATE_USER_REQUEST.email,
        username=CREATE_USER_REQUEST.username,
        password=CREATE_USER_REQUEST.password))
    mock_request.app.get.side_effect = [create_user, auth]
    users_api = UsersAPI()
    response = await users_api.register_user(mock_request)
    create_user.execute.assert_called_with(CREATE_USER_REQUEST)
    auth.generate_token.assert_called_with(USER_ID)
    assert response.status == 201
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(userId=USER_ID, token=TOKEN)


async def test_register_user_should_return_400_if_request_data_is_invalid(create_user, auth):
    mock_request = create_mock_request(data=dict(
        email=CREATE_USER_REQUEST.email,
        username=CREATE_USER_REQUEST.username,
        password=CREATE_USER_REQUEST.password))
    mock_request.app.get.side_effect = [create_user, auth]
    message = "Some Error"
    users_api = UsersAPI()
    create_user.execute.side_effect = ValueError(message)
    response = await users_api.register_user(mock_request)
    assert response.status == 400
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(errors=[message])


async def test_login_should_return_user_id_and_generated_token_if_credentials_match(users, auth):
    users.find_by_credentials.return_value = USER
    mock_request = create_mock_request(data=dict(
        email=USER.email, password=USER.password))
    mock_request.app.get.side_effect = [users, auth]
    users_api = UsersAPI()
    response = await users_api.login(mock_request)
    users.find_by_credentials.assert_called_with(USER.email, USER.password)
    auth.generate_token.assert_called_with(USER_ID)
    assert response.status == 200
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(userId=USER_ID, token=TOKEN)


async def test_login_should_return_400_if_user_does_not_exist(users, auth):
    message = "Invalid login credentials"
    users.find_by_credentials.return_value = None
    mock_request = create_mock_request(data=dict(
        email=USER.email, password=USER.password))
    mock_request.app.get.side_effect = [users, auth]
    users_api = UsersAPI()
    response = await users_api.login(mock_request)
    users.find_by_credentials.assert_called_with(USER.email, USER.password)
    assert response.status == 400
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(errors=[message])


async def test_login_should_return_400_if_password_does_not_match(users, auth):
    message = "Invalid login credentials"
    incorrect_password = "incorrect password"
    users.find_by_credentials.return_value = None
    mock_request = create_mock_request(data=dict(
        email=USER.email, password=incorrect_password))
    mock_request.app.get.side_effect = [users, auth]
    users_api = UsersAPI()
    response = await users_api.login(mock_request)
    users.find_by_credentials.assert_called_with(USER.email, incorrect_password)
    assert response.status == 400
    assert response.content_type == "application/json"
    assert json.loads(response.text) == dict(errors=[message])
