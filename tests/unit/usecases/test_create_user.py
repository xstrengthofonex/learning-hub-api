from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.domain.users import Users, User, UserValidator
from learning_hub.usecases.create_user import CreateUser, CreateUserRequest


USER_ID = str(uuid4())
CREATE_USER_REQUEST = CreateUserRequest(
    email="example@email.com",
    username="username",
    password="password")
USER = User(
    id=USER_ID,
    email=CREATE_USER_REQUEST.email,
    username=CREATE_USER_REQUEST.username,
    password=CREATE_USER_REQUEST.password)


@pytest.fixture
def users():
    return Mock(Users)


@pytest.fixture
def user_validator():
    return Mock(UserValidator)


@pytest.fixture
def create_user(users, id_generator, user_validator):
    create_user = CreateUser(users)
    create_user.user_validator = user_validator
    create_user.id_generator = id_generator
    return create_user


@pytest.fixture(autouse=True)
def setup(id_generator, create_user):
    id_generator.generate.return_value = USER_ID


async def test_create_user_saves_the_user(create_user, users):
    await create_user.execute(CREATE_USER_REQUEST)
    users.add.assert_called_with(USER)


async def test_create_user_returns_user_id_for_created_user(create_user):
    result = await create_user.execute(CREATE_USER_REQUEST)
    assert result.user_id == USER_ID


async def test_raises_value_error_if_create_user_request_is_invalid(create_user, user_validator):
    user_validator.validate.side_effect = ValueError("Some Error")
    with pytest.raises(ValueError):
        await create_user.execute(CREATE_USER_REQUEST)
